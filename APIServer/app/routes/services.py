from datetime import datetime
import time
from fastapi import APIRouter
from sqlalchemy.sql.expression import update
from starlette.requests import Request
from starlette.responses import JSONResponse
from typing import List
import json

from Database.schema import Users,Assets, Notices
from app.models import model as m

router = APIRouter(prefix='/services')

@router.get('/assets', response_model=m.AssetsInfo)
async def get_assets(request: Request):

    item_dict = list()
    for item in Assets.filter().all():
        item_dict.append(dict(currency=item.currency, name_kor=item.name_kor, price=item.price, updated_at = item.updated_at))

    result = dict()
    result["data"] = item_dict

    return result

@router.get('/notices', response_model=m.AssetsInfo)
async def get_notices(request: Request):

    item_dict = list()
    item = Notices.filter().order_by("-reg_date").first()
    item_dict.append(dict(currency = item.currency, title=item.title, link = item.link, reg_date = item.reg_date))

    result = dict()
    result["data"] = item_dict

    return result