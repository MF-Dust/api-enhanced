import logging
import sys
from typing import Any

from config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("pyncmapi")


def log_request(method: str, url: str, status: int, duration_ms: float) -> None:
    """Log HTTP request details."""
    logger.info(f"{method} {url} - {status} ({duration_ms:.2f}ms)")


def log_error(message: str, exc: Exception | None = None, extra: dict[str, Any] | None = None) -> None:
    """Log error with optional exception and extra context."""
    if extra:
        logger.error(f"{message} - {extra}", exc_info=exc)
    else:
        logger.error(message, exc_info=exc)


def log_warning(message: str, extra: dict[str, Any] | None = None) -> None:
    """Log warning with optional extra context."""
    if extra:
        logger.warning(f"{message} - {extra}")
    else:
        logger.warning(message)


def log_info(message: str, extra: dict[str, Any] | None = None) -> None:
    """Log info with optional extra context."""
    if extra:
        logger.info(f"{message} - {extra}")
    else:
        logger.info(message)


def log_debug(message: str, extra: dict[str, Any] | None = None) -> None:
    """Log debug with optional extra context."""
    if extra:
        logger.debug(f"{message} - {extra}")
    else:
        logger.debug(message)
