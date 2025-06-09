from fastapi import WebSocket
from fastapi.encoders import jsonable_encoder
from starlette.websockets import WebSocketState

from app.models.dto.event import Event


async def send_event(event: Event, websocket: WebSocket):
    if websocket.client_state == WebSocketState.CONNECTED:
        await websocket.send_json(jsonable_encoder(event))
