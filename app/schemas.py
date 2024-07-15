from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    password: str

class CreateUser(UserBase):
    pass

class UpdateUser(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    # so far, not required
    # class Config:
    #     orm_mode = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    # class Config:
    #     orm_mode = True
    pass

class PostsVotesResponse(BaseModel):
    Post: PostResponse
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    vote_dir: bool