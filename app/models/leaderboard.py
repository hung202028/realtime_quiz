import asyncio
from typing import Dict
from typing import Optional

from app.config import AppClients
from app.models.connection import SocketConnectionManager
from app.models.dto.leaderboard import LeaderBoardDTO, UserScore


class LeaderboardManager:
    def __init__(
            self,
            connection_manager: SocketConnectionManager,
            app_clients: AppClients,
            refresh_seconds: int = 2
    ):
        self.connection_manager = connection_manager
        self.app_clients = app_clients
        self.refresh_seconds = refresh_seconds
        self._active_tasks: Dict[str, Optional[asyncio.Task]] = {}

    async def _get_data(self, quiz_id: str) -> LeaderBoardDTO:
        scores: dict = await self.app_clients.cache.get_scores(quiz_id)
        user_scores = [
            UserScore(
                user_id=str(user_id),
                score=int(score),
                quiz_id=quiz_id
            ) for user_id, score in scores.items()
        ]

        user_scores.sort(key=lambda x: x.score, reverse=True)
        return LeaderBoardDTO(quiz_id=quiz_id, user_scores=user_scores)

    def _send_queue(self, leaderboard: LeaderBoardDTO):
        self.app_clients.message_queue.publish(
            leaderboard,
            routing_key="quiz.leaderboard.update",
            exchange_params={
                "exchange": "quiz_exchange",
                "exchange_type": "topic",
                "durable": True,
            }
        )

    async def update(self, quiz_id: str):
        try:
            while True:
                if not self.connection_manager.active_connections[quiz_id]:
                    self.app_clients.logger.info(f"No active connections for {quiz_id}")
                    break

                data = await self._get_data(quiz_id)
                self._send_queue(data)
                await asyncio.sleep(self.refresh_seconds)
        except asyncio.CancelledError:
            self.app_clients.logger.info(f"Leaderboard updates cancelled for {quiz_id}")
        except Exception as e:
            self.app_clients.logger.error(f"Leaderboard update error: {str(e)}")
        finally:
            self._active_tasks.pop(quiz_id, None)
