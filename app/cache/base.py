from abc import ABC, abstractmethod


class QuizCache(ABC):
    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def get_scores(self, quiz_id: str):
        pass

    @abstractmethod
    async def init_score(self, user_id: str, quiz_id: str):
        pass

    @abstractmethod
    async def increase_user_score(self, quiz_id: str, user_id: str, score_increase: int):
        pass
