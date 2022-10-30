import time
from utils.api_logger import api_logger
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse


async def access_control(request: Request, call_next):
    request.state.start = time.time()
    request.state.user = None
    request.state.ip = request.client.host
    try:
        response = await call_next(request)
        await api_logger(request=request, response=response)
    except Exception as e:
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e)
        )
        await api_logger(request=request, error=e)
    finally:
        return response
