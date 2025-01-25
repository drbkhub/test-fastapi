from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.domain.user import crud
from database.engine import get_db
from core.domain.user.exceptions import EmailAlreadyExistsError
from core.domain.user.schemas import User, UserCreate, UserUpdate

router = APIRouter()


@router.get("/users/", response_model=list[User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@router.get("/users/{id}", response_model=User)
def read_user(id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.post("/users/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = crud.create_user(db=db, user=user)
        return user
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.delete("/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    if not crud.delete_user(db=db, id=id):
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{id}", response_model=User)
def update_user(id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, id=id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
