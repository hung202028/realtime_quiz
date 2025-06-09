from typing import Dict

from redis.asyncio import Redis

from app.cache.base import QuizCache


class QuizCacheRedis(QuizCache):
    def __init__(self, *args, **kwargs):
        host = kwargs.get("host")
        port = kwargs.get("port")
        decode_response = kwargs.get("decode_response")
        self.redis = Redis(host=host, port=port, decode_responses=decode_response)

    async def get_scores(self, quiz_id: str) -> Dict:
        scores = await self.redis.hgetall(f"quiz:{quiz_id}")
        return scores

    async def init_score(self, user_id: str, quiz_id: str):
        await self.redis.hset(f"quiz:{quiz_id}", user_id, "0")

    async def increase_user_score(self, quiz_id: str, user_id: str, score_increase: int):
        await self.redis.hincrby(f"quiz:{quiz_id}", user_id, score_increase)

    async def close(self):
        await self.redis.aclose()
