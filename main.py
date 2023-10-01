import logging
from typing import List

from fastapi import Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.schemas import UserUpdate

app = FastAPI()

logging = logging.getLogger(__name__)


# User
@app.post(path="/v1/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    logging.info(f"post /v1/users: {user.model_dump_json()}")
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get(path="/v1/users/{user_id}", response_model=schemas.UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    logging.info(f"get /v1/users/{user_id}")

    db_user = crud.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found.")

    return db_user


@app.get(path="/v1/users", response_model=List[schemas.UserResponse])
def get_users(offset: int, limit: int, db: Session = Depends(get_db)):
    logging.info(f"get /v1/users, offset: {offset}, limit: {limit}")
    return crud.get_users(db, skip=offset, limit=limit)


@app.put(path="/v1/users/{user_id}", response_model=schemas.UserResponse)
def get_users(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    logging.info(f"put /v1/users, user: {user.model_dump_json()}")
    return crud.update_user(db, user_id, updated_data=user.model_dump(exclude_unset=True))
