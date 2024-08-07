from fastapi import APIRouter, HTTPException

from .schemas import User, UserReturned, CheckDatesUser

from models import UserModel

from .core import hashing_password, create_or_none_user

from database import create_session


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

    return dates

