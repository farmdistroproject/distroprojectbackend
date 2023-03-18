
from . import schemas
from fastapi import HTTPException,status
from . import helpers

from . import models

from sqlalchemy.orm import Session



class UserCrud():

    @staticmethod
    def create_user(request:schemas.User,db:Session):
        if request.password1 != request.password2:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="passwords do not match")
        if len(request.password1) < 6 :
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="make password 6 characters")

        cleaned_password = helpers.hash_password(request.password1)
        new_user = models.User(email=request.email,password=cleaned_password,first_name=request.first_name,last_name=request.last_name,date_of_birth=request.date_of_birth,phone_number = request.phone_number)



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

    
   


    
