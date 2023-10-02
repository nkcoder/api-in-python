from sqlalchemy import func

from app.persistence.database import SessionLocal as Session
from app.persistence.models import User
from app.schemas.user_schema import UserUpdate, UserCreate


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.user_name == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, updated_data: UserUpdate):
    db.query(User).filter(User.id == user_id).update(updated_data.model_dump(exclude_unset=True))
    db.commit()
    return get_user_by_id(db, user_id)


def delete_user(db: Session, user_id: int):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = user.password + "faked_hash"
    db_user = User(user_name=user.user_name, email=user.email,
                   password=hashed_password,
                   date_registered=func.now())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
