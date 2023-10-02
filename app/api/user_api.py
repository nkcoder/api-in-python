import logging

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.service import user_service
from app.persistence.database import get_db
from app.schemas.user_schema import *

router = APIRouter(
        prefix="/v1/users",
        tags=["User"]
)
logger = logging.getLogger("user router")


# User
@router.post(path="", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    logger.info(f"create user: {user.model_dump_json(exclude={'password'})}")
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db=db, user=user)


@router.get(path="/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"get user by id: {user_id}")

    db_user = user_service.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user


@router.get(path="", response_model=List[UserResponse])
def get_users(offset: int, limit: int, db: Session = Depends(get_db)):
    logger.info(f"get users, offset: {offset}, limit: {limit}")
    return user_service.get_users(db, skip=offset, limit=limit)


@router.put(path="/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    logger.info(f"update user: {user_id}, user: {user.model_dump_json()}")
    return user_service.update_user(db, user_id, updated_data=user)
