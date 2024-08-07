from pydantic import BaseModel


class User(BaseModel):
    name: str | None = 'User'
    age: int | None = None
    email: str
    hashed_password: str


class UserReturned(BaseModel):
    name: str
    age: int | None = None


class CheckDatesUser(BaseModel):
    email: str
    password: str
