from sqlalchemy import DECIMAL, Column, DateTime, Enum, Integer, String, func

from .base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(1024), nullable=False, default="")
    status = Column(
        Enum("pending", "processing", "completed", "cancelled", name="order_status"),
        nullable=False,
        default="pending",
    )
    total_amount = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def __repr__(self):
        return f"<Order(id={self.id}, status='{self.status}', total_amount={self.total_amount})>"
