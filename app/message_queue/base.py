from abc import ABC, abstractmethod

from pydantic import BaseModel


class MessageQueue(ABC):

    @abstractmethod
    def publish(self, data: BaseModel, **kwargs):
        pass
