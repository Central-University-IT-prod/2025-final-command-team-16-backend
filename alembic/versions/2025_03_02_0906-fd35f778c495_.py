"""empty message

Revision ID: fd35f778c495
Revises: 5b6828ce36fb
Create Date: 2025-03-02 09:06:13.841070

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fd35f778c495"
down_revision: str | None = "5b6828ce36fb"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "book_offers",
        "binding",
        existing_type=postgresql.ENUM(
            "Твёрдая обложка", "Мягкая обложка", name="bookbindingtype"
        ),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        "book_offers",
        "size",
        existing_type=postgresql.ENUM(
            "Маленькая", "Стандартная", "Большая", name="booksizetype"
        ),
        type_=sa.String(),
        existing_nullable=True,
    )
    op.alter_column(
        "book_offers",
        "physical_state",
        existing_type=postgresql.ENUM(
            "Новая",
            "Хорошая",
            "С небольшими повреждениями",
            "С существенными повреждениями",
            name="bookstatetype",
        ),
        type_=sa.String(),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "book_offers",
        "physical_state",
        existing_type=sa.String(),
        type_=postgresql.ENUM(
            "Новая",
            "Хорошая",
            "С небольшими повреждениями",
            "С существенными повреждениями",
            name="bookstatetype",
        ),
        existing_nullable=True,
    )
    op.alter_column(
        "book_offers",
        "size",
        existing_type=sa.String(),
        type_=postgresql.ENUM(
            "Маленькая", "Стандартная", "Большая", name="booksizetype"
        ),
        existing_nullable=True,
    )
    op.alter_column(
        "book_offers",
        "binding",
        existing_type=sa.String(),
        type_=postgresql.ENUM(
            "Твёрдая обложка", "Мягкая обложка", name="bookbindingtype"
        ),
        existing_nullable=True,
    )
