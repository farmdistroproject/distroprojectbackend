from pydantic import BaseModel,EmailStr
from datetime import datetime,date,time
from typing import Union,Optional
from fastapi_jwt_auth import AuthJWT


class User(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str
    first_name: str
    last_name:str
    phone_number: int
    dob: date


class UserUpdate(BaseModel):
    email:Union[EmailStr, None]
    username:Union[str, None]
    first_name: Union[str, None]
    last_name:Union[str, None]
    phone_number: Union[str, None]
    dob: Optional[date] = None



class ShowUser(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name:str
    phone_number: str
    dob: date

    class Config():
        orm_mode = True

class Login(BaseModel):
    username:EmailStr
    password:str

class resetPassword(BaseModel):
    username: Optional[str] = None
    email:Optional[EmailStr] = None



class Settings(BaseModel):
    authjwt_secret_key: str = "secret"
    authjwt_token_location:set ={'cookies','headers'}
    authjwt_access_cookie_key:str='access_token'
    authjwt_refresh_cookie_key:str='refresh_token'
    authjwt_cookie_csrf_protect: bool = False
    authjwt_cookie_samesite:str ='lax'

@AuthJWT.load_config
def get_config():
    return Settings()