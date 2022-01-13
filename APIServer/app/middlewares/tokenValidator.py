import time
import re

import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError

from starlette.requests import Request
from starlette.responses import JSONResponse

from app.common.consts import EXCEPT_PATH_LIST, EXCEPT_PATH_REGEX, JWT_SECRET, JWT_ALGORITHM
from app.errors.exceptions import APIException
from app.utils.date_utils import Date
from app.utils.logger import api_logger
from app.models.model import UserToken
from app.errors import exceptions as ex

async def access_control(request: Request, call_next):
    try:
        request.state.req_time = Date.datetime()
        request.state.start = time.time()
        request.state.inspect = None
        request.state.user = None
        request.state.service = None

        ip = request.headers["x-forwarded-for"] if "x-forwarded-for" in request.headers.keys() else request.client.host
        request.state.ip = ip.split(",")[0] if "," in ip else ip
        
        headers = request.headers
        url = request.url.path
        cookie = request.cookies
        
        # Token 검사가 필요없는 Url 확인
        if await url_pattern_check(url, EXCEPT_PATH_REGEX) or url in EXCEPT_PATH_LIST:
            response = await call_next(request)
            await api_logger(request=request, response=response)
            return response
        
        # Header에 있는 JWT 검사
        if "authorization" in headers.keys():
            token_info = await token_decode(access_token=headers.get("Authorization"))
            request.state.user = UserToken(**token_info)
            response = await call_next(request)
            await api_logger(request=request, response=response)
        else:
            raise ex.NotAuthorized()
        
    except Exception as e:
        error = await exception_handler(e)
        error_dict = dict(status=error.status_code, description=error.description)
        response = JSONResponse(status_code=error.status_code, content=error_dict)
        await api_logger(request=request, error=error)

    return response


async def url_pattern_check(path, pattern):
    result = re.match(pattern, path)
    if result:
        return True
    return False

async def token_decode(access_token):
    try:
        access_token = access_token.replace("Bearer ", "")
        payload = jwt.decode(access_token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except ExpiredSignatureError:
        raise ex.TokenExpiredEx()
    except DecodeError:
        raise ex.TokenDecodeEx()
    return payload


async def exception_handler(error: Exception):
    if not isinstance(error, APIException):
        error = APIException(ex=error, description=str(error))
    return error
