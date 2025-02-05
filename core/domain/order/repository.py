from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.domain.order import schemas
from database import models
from database.engine import get_db


class OrderRepository:
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_orders(self, skip: int = 0, limit: int = 10) -> list[models.Order]:
        query = select(models.Order).offset(skip).limit(limit)
        result = await self.session.execute(query)
        orders = result.scalars().all()
        return orders

    async def create_order(self, order: schemas.OrderCreate) -> models.Order:
        db_order = models.Order(
            description=order.description,
            total_amount=order.total_amount,
        )

        self.session.add(db_order)
        await self.session.commit()
        await self.session.refresh(db_order)
        return db_order

    async def delete_order(self, id: int) -> bool:
        db_order = await self.get_order_by_id(id=id)
        if db_order:
            await self.session.delete(db_order)
            await self.session.commit()
            return True
        return False

    async def get_order_by_id(self, id: int) -> models.Order | None:
        stmt = select(models.Order).where(models.Order.id == id)
        return (await self.session.scalars(stmt)).first()

    async def update_order(
        self, id: int, order_update: schemas.OrderUpdate
    ) -> models.Order:
        db_order = await self.get_order_by_id(id=id)
        if not db_order:
            return None

        if db_order.description is not None:
            db_order.description = order_update.description
        if db_order.status is not None:
            db_order.status = order_update.status
        if db_order.total_amount is not None:
            db_order.total_amount = order_update.total_amount

        await self.session.commit()
        await self.session.refresh(db_order)

        return db_order
