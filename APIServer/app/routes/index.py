from datetime import datetime

from fastapi import APIRouter
from starlette.responses import Response

router = APIRouter()

@router.get("/")
async def index():
    current_time = datetime.now()
    return Response(f"Welcom to API Server (Time: {current_time.strftime('%Y.%m.%d %H:%M:%S')})")