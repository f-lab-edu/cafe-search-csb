import logging
import sys
from fastapi.logger import logger as fastapi_logger


def init_fastapi_logger(
    logger: logging.Logger = fastapi_logger,
    console: bool = False,
    logfilename: str = None,
):
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s : %(levelname)-s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)

    if logfilename:
        file_handler = logging.FileHandler(logfilename)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


logger = init_fastapi_logger(console=True)
