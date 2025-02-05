from enum import Enum
from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime


class OrderStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderBase(BaseModel):
    description: str
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime


class Order(OrderBase):
    id: int

    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    description: str
    total_amount: Decimal


class OrderUpdate(BaseModel):
    description: str
    status: OrderStatus
    total_amount: Decimal


class OrderResponse(BaseModel):
    id: int
    description: str
    status: OrderStatus
    total_amount: Decimal
    created_at: datetime
    updated_at: datetime
