from typing import List, Dict

from fastapi import WebSocket, WebSocketDisconnect

from app.config import AppClients
from app.models.dto.event import Event
from app.models.utils import send_event


class SocketConnectionManager:
    def __init__(self, app_clients: AppClients):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.monitor = app_clients.monitor
        self.logger = app_clients.logger

    async def connect(self, websocket: WebSocket, quiz_id: str):
        if quiz_id not in self.active_connections:
            self.active_connections[quiz_id] = []
        self.active_connections[quiz_id].append(websocket)
        self.monitor.record_connection_established()

    async def disconnect(self, websocket: WebSocket, quiz_id: str):
        if quiz_id in self.active_connections:
            try:
                await websocket.close(code=1000)
            except RuntimeError:  # Already closed
                pass
            finally:
                try:
                    self.active_connections[quiz_id].remove(websocket)
                    if not self.active_connections[quiz_id]:
                        self.active_connections.pop(quiz_id)
                    self.monitor.record_connection_terminated()
                except ValueError:
                    pass

    async def broadcast(self, quiz_id: str, event: Event):
        if quiz_id in self.active_connections:
            for websocket in list(self.active_connections[quiz_id]):
                try:
                    await send_event(event, websocket)
                except (WebSocketDisconnect, RuntimeError):
                    await self.disconnect(websocket, quiz_id)
