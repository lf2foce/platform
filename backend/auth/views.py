from typing import List
from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from backend.database.core import get_db
from backend.auth import service
from backend.schemas.user import User, UserCreate
from backend.schemas.item import Item, ItemCreate

user_router = APIRouter()


@user_router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):  # = Depends(get_db):
    db_user = service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return service.create_user(db=db, user=user)


@user_router.get("/", response_model=List[User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = service.get_users(db, skip=skip, limit=limit)
    return users


@user_router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = service.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@user_router.post("/{user_id}/items/", response_model=Item)
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    return service.create_user_item(db=db, item=item, user_id=user_id)


@user_router.get("/items/", response_model=List[Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = service.get_items(db, skip=skip, limit=limit)
    return items


# @user_router.get("/", tags=["users"])
# async def read_users():
#     return [{"username": "Rick"}, {"username": "Morty"}]


# @user_router.get("/me", tags=["users"])
# async def read_user_me():
#     return {"username": "fakecurrentuser"}


# @user_router.get("/{username}", tags=["users"])
# async def read_user(username: str):
#     return {"username": username}
