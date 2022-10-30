import logging
from typing import Optional
from time import time
from utils.init_logger import logger
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response


async def api_logger(
    request: Request,
    response: Optional[Response] = None,
    error: Optional[Exception] = None,
):
    processed_time = time() - request.state.start
    status_code = (
        status.HTTP_500_INTERNAL_SERVER_ERROR if error else response.status_code
    )

    if error:
        error_log = dict(raised=str(error.__class__.__name__), msg=str(error))
    else:
        error_log = None

    user_log = dict(
        client=request.state.ip,
        user=request.state.user.id if request.state.user else None,
    )

    log_dict = dict(
        url=request.url.hostname + request.url.path,
        method=str(request.method),
        statusCode=status_code,
        errorDetail=error_log,
        client=user_log,
        processedTime=str(round(processed_time * 1000, 5)) + "ms",
    )

    if error:
        logger.error(log_dict)
    else:
        logger.info(log_dict)
