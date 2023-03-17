
from . import schemas
from fastapi import HTTPException,status
from .helpers import hash_password

from . import models

from sqlalchemy.orm import Session



class UserCrud():

    @staticmethod
    def create_user(request:schemas.User,db:Session):
        if request.password1 != request.password2:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="passwords do not match")
        if len(request.password1) < 6 :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="make password 6 characters")
        cleaned_password = hash_password(request.password1)

        new_user = models.User(email=request.email,username=request.username,password=cleaned_password)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod

    def update_user(id:int,db:Session,request:schemas.UserUpdate):
        user = db.query(models.User).filter(models.User.id == id)

        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
        user.update(request.dict(exclude_unset=True),synchronize_session=False)
        db.commit()
        return "user updated"

    
    @staticmethod
    def create_user_profile(user:dict(),db:Session,request:schemas.UserProfile):
        # user = db.query(models.User).filter(models.User.id == id)
        userp = db.query(models.UserProfile).filter(models.UserProfile.user_id == user.id).first()
        if userp:
            raise HTTPException(status_code=status.HTTP_207_MULTI_STATUS,detail=f"profile exists {userp}, update")
        user_profile = models.UserProfile(first_name=request.first_name,last_name=request.last_name,dob=request.dob,phone_number = request.phone_number,user_id = user.id)
        db.add(user_profile)
        db.commit()
        db.refresh(user_profile)
        return user_profile


    @staticmethod
    def update_user_profile(user:dict(),db:Session,request:schemas.UserProfileUpdate):
        userp = db.query(models.UserProfile).filter(models.UserProfile.user_id == user.id)
        if not userp:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
        try:
            userp.update(request.dict(exclude_unset=True),synchronize_session=False)
            db.commit()
        except Exception as e:
            return e
        
        return "user updated"  

    

