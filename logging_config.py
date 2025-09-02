import sys
import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        # Retrieve context where the logging call occurred
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())


def setup_logging():
    # Remove default handlers
    logging.root.handlers = []
    logging.root.setLevel(logging.INFO)

    # Intercept standard logging
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    # Redirect Uvicorn and FastAPI logs to Loguru
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure Loguru sink
    logger.remove()
    logger.add(sys.stdout, colorize=True, format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")
