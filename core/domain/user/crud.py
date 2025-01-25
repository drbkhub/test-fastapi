from sqlalchemy.orm import Session

from database import models
from core.domain.user import schemas
from core.domain.user.exceptions import EmailAlreadyExistsError


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    if get_user_by_email(db=db, email=user.email):
        raise EmailAlreadyExistsError("Email already taken")

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password="fakehashed_" + user.password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, id: int):
    db_user = get_user_by_id(db=db, id=id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False


def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def update_user(db: Session, id: int, user_update: schemas.UserUpdate):
    db_user = get_user_by_id(db=db, id=id)
    print(db_user)
    if not db_user:
        return

    if db_user:
        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.is_active is not None:
            db_user.is_active = user_update.is_active

        db.commit()
        db.refresh(db_user)

    return db_user
