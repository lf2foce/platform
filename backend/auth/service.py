from sqlalchemy.orm import Session

# from auth import models
from backend.database.models import User, Item
import backend.schemas.user as user_schema
import backend.schemas.item as item_schema

import sqlparse


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_schema.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: item_schema.ItemCreate, user_id: int):
    # db_item = Item(**item.dict(), owner_id=user_id) # ddang ddunsg
    db_item = Item(
        title=item.title,
        description=item.description,
        owner_id=user_id,
        knowledge=sqlparse.format(item.knowledge, reindent=True, keyword_case="upper"),
    )

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# development nflix
def update(*, db: Session, user: user_schema.User, user_in: user_schema.UserUpdate):
    """Updates a user."""
    user_data = user.dict()

    update_data = user_in.dict(exclude={"password"}, skip_defaults=True)
    for field in user_data:
        if field in update_data:
            setattr(user, field, update_data[field])

    if user_in.password:
        password = bytes(user_in.password, "utf-8")
        user.password = password

    db.commit()
    return user
