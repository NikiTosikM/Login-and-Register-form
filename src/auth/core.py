import bcrypt

from database import create_session

from sqlalchemy import select

from models import UserModel


async def hashing_password(password: str):
    salt = bcrypt.gensalt()
    pw_bytes = password.encode("utf-8")
    password = bcrypt.hashpw(pw_bytes, salt)

    return password

async def create_or_none_user(user: UserModel):
    async for session in create_session():
        query = await session.execute(select(UserModel).where(UserModel.email == user.email))
        user = query.scalars().first()

        return user