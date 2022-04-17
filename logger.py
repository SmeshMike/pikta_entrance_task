import datetime
import logging
import logging.config
import os

logs_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_CONFIG = {
    "version": 1,
    "handlers": {
        "file": {
            "level": "INFO",
            "formatter": "myFormatter",
            "class": "logging.FileHandler",
            "filename": f"{os.path.join(logs_dir,datetime.datetime.now().strftime('%Y%m%d.log'))}",
        },
        "console": {
            "level": "INFO",
            "formatter": "myFormatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "": {"handlers": ["file", "console"], "level": "INFO", "propagate": False},
    },
    "formatters": {"myFormatter": {"format": LOG_FORMAT}},
}
logging.config.dictConfig(LOG_CONFIG)
logging.basicConfig(level=logging.INFO)


def get_logger() -> logging.Logger:
    """Возвращает настроенный логгер."""
    return logging.getLogger()
