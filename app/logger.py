import json
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict


class LogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone(timedelta(hours=7))).strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage()
        }

        if record.exc_info:
            log_entry["exc_info"] = self.formatException(record.exc_info)
        if hasattr(record, "props") and isinstance(record.props, dict):
            log_entry.update(record.props)

        return json.dumps(log_entry)


class Logger:
    _instance = None
    _logger = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self, log_file: str = "logs.json", log_level=logging.INFO, stdout=False):
        self._logger = logging.getLogger("quiz_logger")
        self._logger.setLevel(log_level)

        if not self._logger.handlers:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(LogFormatter())
            self._logger.addHandler(file_handler)

            if stdout:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(LogFormatter())
                self._logger.addHandler(console_handler)

    def _log(self, level: int, msg: str, exc_info: bool = False, extra_props: Optional[Dict] = None):
        extra = {'props': extra_props} if extra_props else None
        self._logger.log(level, msg, exc_info=exc_info, extra=extra)

    def info(self, msg: str, exc_info: bool = False, extra_props: Optional[Dict] = None):
        self._log(logging.INFO, msg, exc_info, extra_props)

    def warn(self, msg: str, exc_info: bool = False, extra_props: Optional[Dict] = None):
        self._log(logging.WARN, msg, exc_info, extra_props)

    def error(self, msg: str, exc_info: bool = True, extra_props: Optional[Dict] = None):
        self._log(logging.ERROR, msg, exc_info, extra_props)
