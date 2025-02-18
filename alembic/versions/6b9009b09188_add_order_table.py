"""Add Order table

Revision ID: 6b9009b09188
Revises: eb84826d5110
Create Date: 2025-02-05 21:30:47.138781

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "6b9009b09188"
down_revision: Union[str, None] = "eb84826d5110"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("description", sa.String(length=1024), nullable=False),
        sa.Column(
            "status",
            sa.Enum(
                "pending", "processing", "completed", "cancelled", name="order_status"
            ),
            nullable=False,
        ),
        sa.Column("total_amount", sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("orders")
    # ### end Alembic commands ###
