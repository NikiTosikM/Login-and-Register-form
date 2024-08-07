from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = 'User'
    age: Mapped[int | None] = None
    email: Mapped[str]
    hashed_password: Mapped[bytes] 


