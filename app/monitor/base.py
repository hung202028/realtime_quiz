from abc import ABC, abstractmethod

from typing import Any


class Monitor(ABC):

    @abstractmethod
    def record_connection_established(self):
        pass

    @abstractmethod
    def record_connection_terminated(self):
        pass

    @abstractmethod
    def time_request(self) -> Any:
        pass
