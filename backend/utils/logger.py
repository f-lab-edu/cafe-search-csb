import logging
from time import time
from typing import Optional
from fastapi.logger import logger
from fastapi.requests import Request
from fastapi.responses import Response

def init_fastapi_logger(logger, console=False, logfilename=None):
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s : %(levelname)-s - %(message)s',
                                 datefmt='%Y-%m-%d %H:%M:%S')

    if console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console)

    if logfilename:
        file_handler = logging.FileHandler(logfilename)
        file_handler.setLevel(logging.ERROR)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
    
fastapi_logger = init_fastapi_logger(logger, console=True)

async def api_logger(request: Request, response: Optional[Response]=None, error: Optional[Exception]=None):
    processed_time = time() - request.state.start
    status_code = error.status_code if error else response.status_code

    if error:
        error_log = dict(
            raised=str(error.__class__.__name__),
            msg=str(error.detail)
        )
    else:
        error_log = None

    user_log = dict(
        client=request.state.ip,
        user=request.state.user.id if request.state.user else None
    )

    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        statusCode=status_code,
        errorDetail=error_log,
        client=user_log,
        processedTime=str(round(processed_time*1000, 5)) + "ms",
    )
    if error:
        fastapi_logger.error(log_dict)
    else:
        fastapi_logger.info(log_dict)

