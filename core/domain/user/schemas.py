from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str
    is_active: bool
    is_admin: bool


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    username: str | None
    is_active: bool | None


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_admin: bool
