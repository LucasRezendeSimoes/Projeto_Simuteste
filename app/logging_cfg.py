import logging
from logging.handlers import RotatingFileHandler
import os
from typing import Dict

def configure_logging(cfg: Dict) -> None:
    """Configura logging com arquivo rotativo e console."""
    level = getattr(logging, cfg.get("level", "INFO").upper())
    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

    # Console
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # File rotating
    os.makedirs("logs", exist_ok=True)
    fh = RotatingFileHandler("logs/app.log", maxBytes=5_000_000, backupCount=3)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
