from enum import Enum
from typing import Any

from pydantic import BaseModel


class EventID(Enum):
    JOIN = "JOIN"
    ERROR = "ERROR"
    SUBMIT_ANSWER = "SUBMIT_ANSWER"
    SCORE_UPDATE = "SCORE_UPDATE"
    LEADERBOARD_UPDATE = "LEADER_BOARD_UPDATE"
    PING = "PING"


class Event(BaseModel):
    event: str
    data: Any = None
