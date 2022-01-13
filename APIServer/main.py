import sys, os
sys.dont_write_bytecode = True
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import uvicorn

from fastapi import FastAPI, Depends
from fastapi.security import APIKeyHeader

from starlette.middleware.base import BaseHTTPMiddleware

from app.middlewares.tokenValidator import access_control
from app.common.config import config
from Database.conn import database
from app.routes import index, auth, users, services

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

def init_app():
    app = FastAPI()
    
    # DB Config 설정
    app = FastAPI()
    database.init_app(app, **config())
    
    # 미들웨어 등록
    app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=access_control) 

    # 라우터 등록
    app.include_router(index.router, tags=["Index"])
    app.include_router(auth.router,tags=["Authentication"], prefix="/api")
    app.include_router(users.router, tags=["Users"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
    app.include_router(services.router, tags=["Services"], prefix="/api", dependencies=[Depends(API_KEY_HEADER)])
    return app
    
app = init_app()
if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.0.104", port=8000, reload=True)
