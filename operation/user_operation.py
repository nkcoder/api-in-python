from app.database import SessionLocal as Session
from app.models import User


def create_user(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_name(db: Session, user_name: str):
    return db.query(User).filter(User.user_name == user_name).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, updated_user: User):
    existing_user = db.query(User).filter(User.id == user_id).first()
    for var, value in vars(updated_user).items():
        setattr(existing_user, var, value)
    db.commit()
    return existing_user


def delete_user(db: Session, user_id: int):
    user_to_delete = db.query(User).filter(User.id == user_id).first()
    db.delete(user_to_delete)
    db.commit()
