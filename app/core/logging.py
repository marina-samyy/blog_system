import logging
import sys
from pathlib import Path
from typing import Any


# ---------- JSON FORMATTER ----------
class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "time": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        # structured fields passed via `extra`
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_record.update(record.extra)

        return str(log_record)


# ---------- LOGGER SETUP ----------
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# avoid duplicate handlers in reload
logger.handlers.clear()

formatter = JsonFormatter()

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# File handler
file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


# ---------- HELPER FUNCTION ----------
def log_event(message: str, **extra: Any):
    logger.info(message, extra={"extra": extra})