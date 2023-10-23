from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserReturn(UserBase):
    id: int
    created_at: datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool


class PostCreate(PostBase):
    published: bool = True


class PostReturn(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserReturn


class PostOut(BaseModel):
    Post: PostReturn
    votes: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
