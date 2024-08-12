from bcrypt import checkpw
import bcrypt

from database import create_session

from sqlalchemy import select, and_
from sqlalchemy.exc import SQLAlchemyError


from models import UserModel

from fastapi import HTTPException, status, \
    Depends, Request

import jwt

from config import setting


async def hashing_password(password: str):
    salt = bcrypt.gensalt()
    pw_bytes = password.encode("utf-8")
    password = bcrypt.hashpw(pw_bytes, salt)

    return password

async def create_or_none_user(user: UserModel):
    async for session in create_session():
        query = select(UserModel).where(UserModel.email == user.email)
        result = await session.execute(query)
        user_request = result.scalars().first()

        return user_request
    

async def check_login(email, password:str):
    try: 
        async for session in create_session():
            query = (select(UserModel)
                .where(
                    UserModel.email==email
                )
            )
            result = await session.execute(query)
            user: UserModel = result.scalars().first()
            if not user or not checkpw(password.encode("utf-8"), user.hashed_password):
                raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, \
                    detail="Check the correctness of the entered data")
            return user
        
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred on the database side")
    

def create_jwt_token(user:UserModel):
    dates = {"id": user.id, "email": user.email}
    token = jwt.encode(dates, setting.SECRET_JWT, setting.JWT_ALGORITHM)

    return token


def get_token(request:Request):
    token = request.cookies.get("token_user")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, \
            detail="The token was not found")

    return token


async def check_token(token = Depends(get_token)):
    dates: dict = jwt.decode(token, setting.SECRET_JWT, \
        algorithms=setting.JWT_ALGORITHM)
    id, email = dates["id"], dates["email"]

    async for session in create_session():
        query = (select(UserModel)
            .where(
                and_(
                    UserModel.id == id,
                    UserModel.email == email    
                )
            )
        )      
        result = await session.execute(query)
        user = result.scalars().first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, \
                detail="User not found")
            
    return token
        
    
