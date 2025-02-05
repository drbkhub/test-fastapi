from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from core.domain.order.schemas import OrderCreate, OrderResponse, OrderUpdate
from core.domain.order.repository import OrderRepository


router = APIRouter()


@router.get("/orders/", response_model=list[OrderResponse])
async def read_orders(
    repository: Annotated[OrderRepository, Depends()],
    skip: int = 0,
    limit: int = 10,
) -> list[OrderResponse]:
    db_orders = await repository.get_orders(skip=skip, limit=limit)
    return [
        OrderResponse(
            id=db_order.id,
            description=db_order.description,
            status=db_order.status,
            total_amount=db_order.total_amount,
            created_at=db_order.created_at,
            updated_at=db_order.updated_at,
        )
        for db_order in db_orders
    ]


@router.get("/orders/{id}", response_model=OrderResponse)
async def read_order(
    repository: Annotated[OrderRepository, Depends()],
    id: int,
) -> OrderResponse:
    db_order = await repository.get_order_by_id(id=id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return OrderResponse(
        id=db_order.id,
        description=db_order.description,
        status=db_order.status,
        total_amount=db_order.total_amount,
        created_at=db_order.created_at,
        updated_at=db_order.updated_at,
    )


@router.post("/orders/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate, repository: Annotated[OrderRepository, Depends()]
) -> OrderResponse:
    db_order = await repository.create_order(order=order)
    return OrderResponse(
        id=db_order.id,
        description=db_order.description,
        status=db_order.status,
        total_amount=db_order.total_amount,
        created_at=db_order.created_at,
        updated_at=db_order.updated_at,
    )


@router.delete("/orders/{id}")
async def delete_order(
    repository: Annotated[OrderRepository, Depends()],
    id: int,
) -> None:
    if not await repository.delete_order(id=id):
        raise HTTPException(status_code=404, detail="Order not found")


@router.put("/orders/{id}", response_model=OrderResponse)
async def update_order(
    repository: Annotated[OrderRepository, Depends()],
    id: int,
    order_update: OrderUpdate,
) -> OrderRepository:
    db_order = await repository.update_order(id=id, order_update=order_update)
    if db_order is None:
        raise HTTPException(status_code=404, detail="Order not fount")
    return OrderResponse(
        id=db_order.id,
        description=db_order.description,
        status=db_order.status,
        total_amount=db_order.total_amount,
        created_at=db_order.created_at,
        updated_at=db_order.updated_at,
    )
