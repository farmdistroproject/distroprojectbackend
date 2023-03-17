from fastapi import APIRouter,status,HTTPException,Depends,Response,Cookie,Header,BackgroundTasks
from sqlalchemy.orm import Session
from config.database import get_db
from . import models
from .helpers import get_user_by_email,verify_password,verification_code,verification_email,get_current_user
from . import  schemas
from fastapi_mail import FastMail,MessageSchema
from config.email import env_config

from fastapi_jwt_auth import AuthJWT
from .crud import UserCrud
from datetime import timedelta



router = APIRouter(prefix="/api/v1/auth",tags=['auth'])

authjwt_secret_key = "random"
SECRET_KEY='secret'
ALGORITHM='HS256'
ACCESS_TOKEN_LIFETIME_MINUTES= 43200
REFRESH_TOKEN_LIFETIME=14
access_cookies_time=ACCESS_TOKEN_LIFETIME_MINUTES * 60
refresh_cookies_time=REFRESH_TOKEN_LIFETIME*3600*24


@router.post("/signup",status_code=status.HTTP_201_CREATED)
async def create_user(request:schemas.User,task:BackgroundTasks,db:Session=Depends(get_db)):
    verify = get_user_by_email(email=request.email,db=db,model=models.User)
    if verify:
        raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,detail="user with email exists")
    new_user = UserCrud.create_user(request,db)
    token = verification_code(new_user.email)
    message = MessageSchema(
        subject="Account Verification Email",
        recipients=[new_user.email], 
        template_body={'token':token, 'user':f'{new_user.username}',},
        subtype='html',
        )
    fm = FastMail(env_config)
    task.add_task(fm.send_message, message, template_name="verify_email.html")
    return {"message":"email verification sent","user":new_user}








@router.post('/resend-email/')
def resend_email_verification_code(task:BackgroundTasks,email:str, db:Session=Depends(get_db)):
    try:
        User=get_user_by_email(email=email,db=db,model=models.User)
        if User.email_verified:
            raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,detail="your email is verified")
        token=verification_code(User.email) 
        message=MessageSchema(
            subject='Account Verification Email',
            recipients=[User.email],
            template_body={'token':token, 'user':f'{User.username}'},
            subtype='html'
        )
        f=FastMail(env_config)
        task.add_task(f.send_message, message, template_name='verify_email.html')
        return {'message':'verification code sent'}
    except:
        raise HTTPException(detail='user with this email does not exists', status_code=400)







    
 
@router.post("/login",)
async def login_in(response:Response,request:schemas.Login,db:Session = Depends(get_db),Authorize:AuthJWT=Depends()):
    """logs user in and return access and refresh tokens"""
    user = get_user_by_email(email=request.username,db=db,model=models.User)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Credentials")
    if not verify_password(request.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Invalid Password")

    access_token=Authorize.create_access_token(subject=user.email, expires_time=timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES))
    refresh_token=Authorize.create_refresh_token(subject=user.email, expires_time=timedelta(days=REFRESH_TOKEN_LIFETIME))
    response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
    response.set_cookie(key='refresh_token',value=refresh_token, expires=refresh_cookies_time, max_age=refresh_cookies_time, httponly=True)
    return {'access_token':access_token, 'refresh_token':refresh_token, 'user':user}
    




@router.post('/refresh-token', summary='new access token')
def refresh_token(response:Response,Authorization:AuthJWT=Depends(), refresh_token:str=Cookie(default=None), Bearer:str=Header(default=None)):
    '''
    pass the refresh token giving during login in the header or sent with the cookie.
    '''
    exception=HTTPException(status_code=401, detail='invalid refresh token or token has expired')
    try:
        Authorization.jwt_refresh_token_required()
        current_user=Authorization.get_jwt_subject()
        access_token=Authorization.create_access_token(current_user)
        response.set_cookie(key='access_token',value=access_token, expires=access_cookies_time, max_age=access_cookies_time, httponly=True)
        return {'access_token':access_token}
    except:
        raise exception



@router.get('/verify-email/',status_code=status.HTTP_202_ACCEPTED)
async def verify_email_code(key:str, db:Session=Depends(get_db)):
    tok = key
    dd = verification_email(token=tok,db=db,model=models.User)
    status = {
        "status_code":200,
        "message": "email verified" if dd else "not verified"
    }
    return status





#reset password
@router.post("/reset-password")
# schemas.
async def reset_password(request:schemas.resetPassword):
    pass


@router.post("/set-profile",status_code=status.HTTP_201_CREATED)
async def create_user_profile_route(request:schemas.UserProfile,userr:dict = Depends(get_current_user),db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == userr.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="user not found")
    response = UserCrud.create_user_profile(user=user,db=db,request=request)
    return response


@router.patch("/update-profile/",status_code=status.HTTP_200_OK)
async def update_user_profile_route(request:schemas.UserProfileUpdate,userr:dict = Depends(get_current_user),db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == userr.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="user not found")
    response = UserCrud.update_user_profile(user=user,db=db,request=request)
    return response


# @router.patch("/update",status_code=status.HTTP_200_OK)
# async def update_user_profile_route(request:schemas.UserUpdate,userr:dict = Depends(get_current_user),db : Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == userr.id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="user not found")
#     response = UserCrud.update_user(id=user.id,db=db,request=request)
#     return response


@router.get("/get-profile",status_code=status.HTTP_200_OK)
async def get_user_profile(userr:dict = Depends(get_current_user),db : Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == userr.id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="user not found")
    response = {
        "user":{
        "username":user.username,
        "email":user.email
        },
        "profile":user.profile

    }
    return response