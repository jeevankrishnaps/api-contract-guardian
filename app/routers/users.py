from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate, UserOut

router=APIRouter(prefix="/v1/users",tags=["users"])

fake_db:dict[int,UserOut]={}
next_id=1

@router.post("",response_model=UserOut,status_code=status.HTTP_201_CREATED)
def create_user(payload:UserCreate):
    global next_id
    user=UserOut(id=next_id,is_active=True,**payload.model_dump())
    fake_db[next_id]=user
    next_id+=1
    return user

@router.get("/{user_id}",response_model=UserOut)
def get_user(user_id:int):
    user=fake_db.get(user_id)
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user

@router.get("",response_model=list[UserOut])
def list_users():
    return list(fake_db.values())

@router.delete("/{user_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id:int):
    if user_id not in fake_db:
        raise HTTPException(status_code=404,detail="User not found")
    del fake_db[user_id]
