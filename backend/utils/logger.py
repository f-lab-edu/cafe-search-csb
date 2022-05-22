import json
import logging
from datetime import datetime, timedelta
from time import time
from typing import Optional
from fastapi.logger import logger
from fastapi.requests import Request
from fastapi.responses import Response

def init_fastapi_logger(logger):
    logger.setLevel(logging.INFO)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(console)
    return logger
    
logger = init_fastapi_logger(logger)

async def api_logger(request: Request, response: Optional[Response]=None, error: Optional[Exception]=None):
    time_format="%Y/%M/%d %H:%M:%S"
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
        datetimeUTC=datetime.utcnow().strftime(time_format),
        datetimeKST=(datetime.utcnow() + timedelta(hours=9)).strftime(time_format)
    )
    if error:
        logger.error(json.dumps(log_dict))
    else:
        logger.info(json.dumps(log_dict))

