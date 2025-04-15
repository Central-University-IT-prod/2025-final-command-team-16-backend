"""empty message

Revision ID: cb3a98e6139a
Revises: 094c81f45ee6
Create Date: 2025-03-01 13:20:07.758449

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "cb3a98e6139a"
down_revision: str | None = "094c81f45ee6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "book_offers",
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("author", sa.String(length=50), nullable=False),
        sa.Column("genre", sa.String(length=100), nullable=True),
        sa.Column("publisher_name", sa.String(), nullable=True),
        sa.Column("language", sa.String(length=30), nullable=True),
        sa.Column(
            "binding",
            sa.Enum("Твёрдая обложка", "Мягкая обложка", name="bookbindingtype"),
            nullable=True,
        ),
        sa.Column("pages_number", sa.Integer(), nullable=True),
        sa.Column(
            "size",
            sa.Enum("Маленькая", "Стандартная", "Большая", name="booksizetype"),
            nullable=True,
        ),
        sa.Column(
            "physical_state",
            sa.Enum(
                "Новая",
                "Хорошая",
                "С небольшими повреждениями",
                "С существенными повреждениями",
                name="bookstatetype",
            ),
            nullable=True,
        ),
        sa.Column("point_id", sa.Integer(), nullable=False),
        sa.Column("main_image_url", sa.String(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["point_id"],
            ["points.id"],
            name=op.f("fk_book_offers_point_id_points"),
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_book_offers")),
        sa.UniqueConstraint("id", name=op.f("uq_book_offers_id")),
    )
    op.create_unique_constraint(op.f("uq_points_id"), "points", ["id"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_points_id"), "points", type_="unique")
    op.drop_table("book_offers")
