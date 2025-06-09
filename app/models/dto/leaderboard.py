from typing import List

from pydantic import BaseModel

from app.models.dto.quiz import UserScore


class LeaderBoardDTO(BaseModel):
    quiz_id: str
    user_scores: List[UserScore]
