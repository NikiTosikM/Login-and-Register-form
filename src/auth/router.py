from fastapi import APIRouter, HTTPException, \
     Response, Depends

from .schemas import User, UserReturned, CheckDatesUser

from models import UserModel

from .core import hashing_password, create_or_none_user, \
    check_login, create_jwt_token, check_token

from database import create_session

import logging


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", response_model=UserReturned)
async def register(dates: User):
    user = await create_or_none_user(dates)
    if user:
        raise HTTPException(status_code=400, detail="This user is already registered")
    
    hashed_password = await hashing_password(dates.hashed_password)

    async for session in create_session():
        query = UserModel(
            name = dates.name,
            age = dates.age,
            email = dates.email,
            hashed_password = hashed_password
        )
        session.add(query)
        await session.commit()

    logger.info('Пользователь зарегистрировался')

    return dates


@router.post("/login")
async def login(dates:CheckDatesUser, responce:Response = Response()):
    user_dates = dates.model_dump()
    email, password = user_dates['email'], user_dates['password']
    user:UserModel = await check_login(email, password)
    token = create_jwt_token(user)
    responce.set_cookie(key="token_user", value=token, path="/")

    logger.info('Пользователь вошел в систему')

    return {"status": "ok", "message": f"{user.name} вошел в систему"}


@router.get("/logout")
async def logout(responce:Response):
    responce.delete_cookie(key="token_user")

    logger.info('Пользователь вышел из системы')

    return {"message": "User logged out"}


@router.get("/request") 
async def token_verification(token=Depends(check_token)):
    return {"status": "ok"}
    
    
    

    

