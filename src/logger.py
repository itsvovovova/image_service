from logging import getLogger, basicConfig, DEBUG

logger = getLogger(__name__)

basicConfig(
    level=DEBUG,
    format="{asctime} | {module: 12.12s} | {lineno: 4d} | "
           "{process} | {threadName} | {levelname: 4.4s}| {message}",
    style='{'
)