import logging

from settings import LOG_LEVEL


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL),
)

logger = logging.getLogger(__name__)
