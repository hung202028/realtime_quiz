# utils/dependencies.py
from dotenv import load_dotenv

from app.config import AppConfigs, AppClients
from app.models.connection import SocketConnectionManager
from app.models.quiz.handler import QuizHandler


class DependencyContainer:
    def __init__(self):
        self._configs = self._init_config()
        self._clients = self._init_client()
        self._socket_manager = SocketConnectionManager(self._clients)
        self._quiz_handler = QuizHandler(self._clients, self._socket_manager)

    def _init_config(self) -> AppConfigs:
        load_dotenv(override=True)
        return AppConfigs()

    def _init_client(self) -> AppClients:
        return AppClients(self._configs)

    def get_configs(self) -> AppConfigs:
        return self._configs

    def get_clients(self) -> AppClients:
        return self._clients

    def get_socket_manager(self) -> SocketConnectionManager:
        return self._socket_manager


container = DependencyContainer()


def get_config() -> AppConfigs:
    return container.get_configs()


def get_clients() -> AppClients:
    return container.get_clients()


def get_socket_manager() -> SocketConnectionManager:
    return container.get_socket_manager()


def get_quiz_handler() -> QuizHandler:
    return container._quiz_handler
