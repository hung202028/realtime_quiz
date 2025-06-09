from abc import ABC, abstractmethod

from app.models.dto.validate import ValidateDTO


class Validator(ABC):

    @abstractmethod
    def validate_quiz(self, quiz_id: str) -> ValidateDTO:
        pass

    @abstractmethod
    def validate_user(self, user_id: str) -> ValidateDTO:
        pass

    @abstractmethod
    def validate_answer(self, answer: str) -> ValidateDTO:
        pass
