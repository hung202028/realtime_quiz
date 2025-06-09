import random

from app.config import AppClients


class ScoreManager:
    def __init__(self, app_clients: AppClients):
        self.app_clients = app_clients

    def rate_answer(self, answer: str) -> int:
        return random.randint(1, 10)

    async def increase_score(self, quiz_id: str, user_id: str, inc_score: int):
        await self.app_clients.cache.increase_user_score(quiz_id, user_id, inc_score)
