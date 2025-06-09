import asyncio
from contextlib import suppress
from typing import Optional

from fastapi import WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from app.config import AppClients
from app.models.connection import SocketConnectionManager
from app.models.dto.event import Event, EventID
from app.models.dto.quiz import UserScore
from app.models.leaderboard import LeaderboardManager
from app.models.mock import MockValidate
from app.models.quiz.validator import Validator
from app.models.score import ScoreManager
from app.models.utils import send_event


class QuizHandler:
    def __init__(self, app_clients: AppClients, connection_manager: SocketConnectionManager):
        self.app_clients = app_clients
        self.connection_manager = connection_manager
        self.validator: Validator = MockValidate()
        self.leaderboard_manager = LeaderboardManager(self.connection_manager, self.app_clients)
        self.score_manager = ScoreManager(self.app_clients)
        self.active_tasks: dict[str, asyncio.Task] = {}
        self._heartbeat_interval = 30  # Seconds for ping/pong

    async def process(self, ws: WebSocket, quiz_id: str):
        user_id: Optional[str] = None
        heartbeat_task: Optional[asyncio.Task] = None

        try:
            await ws.accept()
            user_id = ws.query_params.get("user_id") or f"anon-{id(ws)}"

            quiz_validate = self.validator.validate_quiz(quiz_id)
            if quiz_validate.has_error:
                await send_event(Event(event=EventID.ERROR.value, data=quiz_validate))
                await ws.close(code=4001)
                return

            await self.connection_manager.connect(ws, quiz_id)
            await self.app_clients.cache.init_score(user_id, quiz_id)

            await send_event(
                Event(
                    event=EventID.JOIN.value,
                    data=UserScore(quiz_id=quiz_id, user_id=user_id, score=0)
                ),
                ws
            )

            # Start leaderboard updates
            await self._manage_leaderboard_task(quiz_id)

            # Main processing loop
            heartbeat_task = asyncio.create_task(self._send_heartbeat(ws))
            await self._message_loop(ws, quiz_id, user_id)

        except WebSocketDisconnect:
            self.app_clients.logger.info(f"Client disconnected: {user_id}")
        except Exception as e:
            self.app_clients.logger.error(f"Handler error: {str(e)}", exc_info=True)
            await send_event(
                Event(
                    event=EventID.ERROR.value,
                    data={"message": "Internal server error"}
                ),
                ws
            )
        finally:
            with suppress(Exception):
                if heartbeat_task:
                    heartbeat_task.cancel()
                await self.connection_manager.disconnect(ws, quiz_id)
                await self._cleanup_leaderboard(quiz_id)

    async def _message_loop(self, ws: WebSocket, quiz_id: str, user_id: str):
        while ws.client_state == WebSocketState.CONNECTED:
            try:
                payload = await ws.receive_json()
                await self._handle_payload(payload, quiz_id, user_id, ws)
            except (WebSocketDisconnect, RuntimeError):
                break
            except Exception as e:
                self.app_clients.logger.error(f"Message processing error: {str(e)}")
                await send_event(
                    Event(
                        event=EventID.ERROR.value,
                        data={"message": "Invalid message format"}
                    ),
                    ws
                )

    async def _handle_payload(self, payload: dict, quiz_id: str, user_id: str, ws: WebSocket):
        answer = payload.get("answer", "")
        if payload.get("event") == EventID.SUBMIT_ANSWER.value:
            answer_score = self.score_manager.rate_answer(answer)
            await self.score_manager.increase_score(quiz_id, user_id, answer_score)
            await send_event(
                Event(
                    event=EventID.SUBMIT_ANSWER.value,
                    data={"user_id": user_id}
                ),
                ws
            )

    async def _manage_leaderboard_task(self, quiz_id: str):
        if quiz_id not in self.active_tasks or self.active_tasks[quiz_id].done():
            self.active_tasks[quiz_id] = asyncio.create_task(self.leaderboard_manager.update(quiz_id))

    async def _cleanup_leaderboard(self, quiz_id: str):
        """Clean up leaderboard tasks when connections drop"""
        if quiz_id in self.connection_manager.active_connections:
            if not self.connection_manager.active_connections[quiz_id]:
                if task := self.active_tasks.get(quiz_id):
                    task.cancel()
                    with suppress(asyncio.CancelledError):
                        await task
                    del self.active_tasks[quiz_id]

    async def _send_heartbeat(self, ws: WebSocket):
        """Maintain connection with periodic pings"""
        while ws.client_state == WebSocketState.CONNECTED:
            await asyncio.sleep(self._heartbeat_interval)
            with suppress(RuntimeError):
                await send_event(Event(event=EventID.PING.value, data={}), ws)
