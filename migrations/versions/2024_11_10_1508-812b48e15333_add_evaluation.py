"""add evaluation

Revision ID: 812b48e15333
Revises: 0da9eeb845ed
Create Date: 2024-11-10 15:08:21.183651

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "812b48e15333"
down_revision: Union[str, None] = "0da9eeb845ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Создаём тип ENUM
    op.execute(
        """
    CREATE TYPE eventresultstatus AS ENUM ('PROGRESS', 'COMPLETED', 'RATED');
    """
    )

    # Создаём таблицу 'evaluations'
    op.create_table(
        "evaluations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mentor_id", sa.Integer(), nullable=False),
        sa.Column("result_id", sa.Integer(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("comment", sa.String(length=128), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["mentor_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["result_id"], ["event_results.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Добавляем колонку 'status' с типом 'eventresultstatus'
    op.add_column(
        "event_results",
        sa.Column(
            "status",
            sa.Enum("PROGRESS", "COMPLETED", "RATED", name="eventresultstatus"),
            nullable=False,
        ),
    )

    # Удаляем старую колонку 'is_completed'
    op.drop_column("event_results", "is_completed")


def downgrade() -> None:
    # Удаляем колонку 'status'
    op.drop_column("event_results", "status")

    # Удаляем таблицу 'evaluations'
    op.drop_table("evaluations")

    # Удаляем тип ENUM 'eventresultstatus'
    op.execute("DROP TYPE eventresultstatus;")

    # Восстанавливаем старую колонку 'is_completed'
    op.add_column(
        "event_results", sa.Column("is_completed", sa.Boolean(), nullable=False)
    )
