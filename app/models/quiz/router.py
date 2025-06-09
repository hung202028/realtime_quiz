from fastapi import APIRouter, WebSocket
from fastapi.params import Depends

from app.models.dependency import get_quiz_handler
from app.models.quiz.handler import QuizHandler

router = APIRouter(prefix="/quiz")


@router.websocket("/{quiz_id}")
async def join_quiz(
        quiz_id: str,
        websocket: WebSocket,
        handler: QuizHandler = Depends(get_quiz_handler)):
    await handler.process(websocket, quiz_id)
