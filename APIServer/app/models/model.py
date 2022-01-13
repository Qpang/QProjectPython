from typing import List
from pydantic.main import BaseModel

#Request
class UserRegister(BaseModel):
    email: str = None
    password: str = None
    name: str = None 
class UserLogin(BaseModel):
    email:str =None
    password: str = None
    
#Reponse 
class HttpResponse(BaseModel):
    status_code : str = "200"
    description : str = "Success"
    class Config:
        orm_mode = True
    
class UserInfo(HttpResponse):
    id: int
    email: str = None
    name: str = None

class AssetsInfo(HttpResponse):
    data : list = None

    
#Object
class UserToken(BaseModel):
    id: int
    email: str = None
    name: str = None
    phone_number: str = None
    profile_img: str = None
    sns_type: str = None

    class Config:
        orm_mode = True