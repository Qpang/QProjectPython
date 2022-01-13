from dataclasses import dataclass
from urllib.parse import quote  

@dataclass
class Config:
    DB_URL: str = 'mysql+pymysql://root:%s@192.168.0.132:3306/qproject?charset=utf8' %quote('Rbdlf1749!@#')
    DB_ECHO:bool = False
    DB_POOL_RECYCLE:int = 900

def config():
    return Config.__dict__


