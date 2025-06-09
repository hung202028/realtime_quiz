from typing import Optional

from pydantic import BaseModel


class UserScore(BaseModel):
    user_id: str
    score: int
    quiz_id: Optional[str] = None


class UserAnswer(BaseModel):
    answer: Optional[str] = None
    user_id: Optional[str] = None
    quiz_id: Optional[str] = None
