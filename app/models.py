from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum #Restricts a field to predefined values

class UserRole(str,Enum):
    admin="admin"
    member="member"
    guest="guest"

class UserCreate(BaseModel):
    username:str=Field(...,min_length=3,max_length=30)
    email:str
    role:UserRole=UserRole.member

class UserOut(BaseModel):
    id:int
    user_name:str
    email:str
    role:UserRole
    is_active:bool=True


