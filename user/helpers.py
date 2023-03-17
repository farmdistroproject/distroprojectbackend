from fastapi import status,HTTPException,Cookie,Header,Depends,UploadFile,File,Body
from datetime import timedelta,timezone,datetime
from jose import JWTError,jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from passlib.context import CryptContext
from .crud import UserCrud
from . import  models
from sqlalchemy.orm import Session
from PIL import Image
import secrets
from fastapi_jwt_auth import AuthJWT
import uuid
from config.database import get_db

import os
from dotenv import load_dotenv
load_dotenv()



pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")

SECRET_KEY='secret'
ALGORITHM='HS256'


def hash_password(password):
    hashed_password = pwd_context.hash(password)
    return hashed_password


def verify_password(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)



def get_user_by_email(email,db:Session,model):
    user = db.query(model).filter(model.email == email).first()
    return user


def get_user_by_id(id:int,db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user
   


def get_current_user(Authorize:AuthJWT=Depends(), db:Session=Depends(get_db), access_token:str=Cookie(default=None),Bearer=Header(default=None)):
    exception=HTTPException(status_code=401, detail='invalid access token or access token has expired', headers={'WWW-Authenticate': 'Bearer'})

    """
        this function uses python fastapi_jwt and its login route is api/v1/login/v2
    """

    try:
        Authorize.jwt_required()
        user_email=Authorize.get_jwt_subject()
        user=get_user_by_email(user_email,db,model=models.User)
        return user
    except:
        raise exception


def generate_uuid(name):
    name = uuid.uuid4()
    return name





async def get_image_url(file: UploadFile = File(...),user:dict = Depends()):
    FILEPATH = "./media/profile_image/"
    filename = file.filename
    ext = filename.split(".")[1]
    if ext not in ['png', 'jpg','webp']:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Image type not allowed")
    token_name= user.username+"_"+"profile_image"+"_"+secrets.token_urlsafe(4)+"."+ext
    generated_name=FILEPATH + token_name
    file_content= await file.read()

    with open(generated_name, 'wb') as file:
        file.write(file_content)

    # PILLOW IMAGE RESIZE
    img = Image.open(generated_name)
    resized_image = img.resize(size=(500,500))
    resized_image.save(generated_name)
    
    file.close()
    file_url = generated_name[1:]
    return file_url



def verification_code(email):
    data={'sub':email, 'type':'verify_email_code', 'exp':datetime.now(tz=timezone.utc)+timedelta(minutes=15)}
    encoded=jwt.encode(data,SECRET_KEY, algorithm=ALGORITHM)
    return encoded


def verification_email(token, db:Session,model):
    exception= HTTPException(status_code=400,  detail='invalid token or token has expired')
    userexception= HTTPException(status_code=400,  detail='no user')
    try:
        payload = jwt.decode(token,'secret',algorithms='HS256')
        user = db.query(model).filter(model.email == payload.get('sub')).first()
        if payload.get('type') != 'verify_email_code':
            raise exception
        elif not user:
            raise userexception 
        user.email_verified = True
        db.commit()
        return {"payload":payload,"user":user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY,detail=e)
    
  


#tf

def get_google_auth(token:str, db:Session=Depends(get_db)):
    try:
        
        token= id_token.verify_oauth2_token(token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))
        user=get_user_by_email(email=token['email'],db=db,model=models.User)
        if user:
            return user
        else:
            user=models.User(email=token['email'], email_verified=True,google_id=token['sub'], password=hash_password(token['sub']),first_name=token['family_name'], last_name=token['given_name'])
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'{e}')