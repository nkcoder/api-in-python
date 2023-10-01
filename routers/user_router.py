import logging
from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

router = APIRouter(
        prefix="/v1/users",
        tags=["User"]
)
logger = logging.getLogger("user router")


# User
@router.post(path="", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logger.info(f"create user: {user.model_dump_json(exclude={'password'})}")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get(path="/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    logger.info(f"get user by id: {user_id}")

    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user


@router.get(path="", response_model=List[schemas.UserResponse])
def get_users(offset: int, limit: int, db: Session = Depends(get_db)):
    logger.info(f"get users, offset: {offset}, limit: {limit}")
    return crud.get_users(db, skip=offset, limit=limit)


@router.put(path="/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    logger.info(f"update user: {user_id}, user: {user.model_dump_json()}")
    return crud.update_user(db, user_id, updated_data=user)
