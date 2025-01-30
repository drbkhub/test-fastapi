from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from core.domain.user.repository import UserRepository
from core.domain.user.exceptions import EmailAlreadyExistsError
from core.domain.user.schemas import UserCreate, UserUpdate, UserResponse

router = APIRouter()


@router.get("/users/", response_model=list[UserResponse])
async def read_users(
    repository: Annotated[UserRepository, Depends()],
    skip: int = 0,
    limit: int = 10,
) -> list[UserResponse]:
    db_users = await repository.get_users(skip=skip, limit=limit)
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
async def read_user(
    repository: Annotated[UserRepository, Depends()], id: int
) -> UserResponse:
    db_user = await repository.get_user_by_id(id=id)
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
    repository: Annotated[UserRepository, Depends()], user: UserCreate
) -> UserResponse:
    try:
        db_user = await repository.create_user(user=user)

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
async def delete_user(
    repository: Annotated[UserRepository, Depends()], id: int
) -> None:
    if not await repository.delete_user(id=id):
        raise HTTPException(status_code=404, detail="User not found")


@router.put("/users/{id}", response_model=UserResponse)
async def update_user(
    repository: Annotated[UserRepository, Depends()], id: int, user_update: UserUpdate
) -> UserResponse:
    db_user = await repository.update_user(id=id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
        is_admin=db_user.is_admin,
    )
