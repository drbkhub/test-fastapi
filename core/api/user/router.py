from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.user import crud
from database.engine import get_db
from core.domain.user.exceptions import EmailAlreadyExistsError
from core.domain.user.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.get("/users/", response_model=list[UserResponse])
async def read_users(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
) -> list[UserResponse]:
    db_users = await crud.get_users(db=db, skip=skip, limit=limit)
    return [
        UserResponse(
            id=db_user.id,
            username=db_user.username,
            email=db_user.email,
            is_active=db_user.is_active,
            is_admin=db_user.is_admin,
        )
        for db_user in db_users
    ]


@router.get("/users/{id}", response_model=UserResponse)
async def read_user(id: int, db: AsyncSession = Depends(get_db)) -> UserResponse:
    db_user = await crud.get_user_by_id(db=db, id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_admin=db_user.is_admin,
    )


@router.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserCreate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    try:
        db_user = await crud.create_user(db=db, user=user)

    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_admin=db_user.is_admin,
    )


@router.delete("/users/{id}")
async def delete_user(id: int, db: AsyncSession = Depends(get_db)) -> None:
    if not await crud.delete_user(db=db, id=id):
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{id}", response_model=UserResponse)
async def update_user(
    id: int, user_update: UserUpdate, db: AsyncSession = Depends(get_db)
) -> UserResponse:
    db_user = await crud.update_user(db=db, id=id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_admin=db_user.is_admin,
    )
