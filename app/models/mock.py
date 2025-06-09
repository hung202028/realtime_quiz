import random

from app.models.dto.validate import ValidateDTO
from app.models.quiz.validator import Validator


class MockValidate(Validator):
    def validate_quiz(self, quiz_id: str) -> ValidateDTO:
        result = ValidateDTO()

        if random.randint(1, 100) % 100 == 0:
            result.has_error = True
            result.error_msg = f"Invalid quiz ID: {quiz_id}"

        return result

    def validate_user(self, user_id: str) -> ValidateDTO:
        result = ValidateDTO()

        if not user_id or random.randint(1, 100) % 2 == 0:
            result.has_error = True
            result.error_msg = f"User id not found: {user_id}"

        return result

    def validate_answer(self, answer: str) -> ValidateDTO:
        result = ValidateDTO()

        if random.randint(1, 100) % 9 == 0:
            result.has_error = True
            result.error_msg = f"Invalid answer: {answer}"

        return result
