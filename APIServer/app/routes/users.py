from datetime import datetime
import time
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse

from Database.schema import Users
from app.models.model import UserInfo, HttpResponse

router = APIRouter(prefix='/user')

@router.get('/me', response_model=UserInfo)
async def get_me(request: Request):
    user = request.state.user
    user_info = Users.get(id=user.id)
    return user_info

@router.put('/me', response_model=UserInfo)
async def update_me(name :str, request: Request):
    user = request.state.user
    Users.filter(id=user.id).update(auto_commit=True, name = name)
    user_data = Users.get(id=user.id)
    return user_data;

@router.delete('/me')
async def delete_me(request: Request):
    user = request.state.user
    Users.filter(id=user.id).delete(auto_commit=True)
    return HttpResponse()


@router.post('/me/tradehistory', response_model=UserInfo)
async def create_tradehistory(name :str, request: Request):
    user = request.state.user
    Users.filter(id=user.id).update(auto_commit=True, name = name)
    user_data = Users.get(id=user.id)
    return user_data;