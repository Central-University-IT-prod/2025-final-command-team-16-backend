"""empty message

Revision ID: 126c22095be9
Revises: 20c0eddf648e
Create Date: 2025-03-02 10:25:30.125281

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "126c22095be9"
down_revision: str | None = "20c0eddf648e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "book_main_images",
        sa.Column("url", sa.String(length=250), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_book_main_images")),
        sa.UniqueConstraint("id", name=op.f("uq_book_main_images_id")),
    )
    op.add_column(
        "book_offers", sa.Column("main_image_id", sa.Integer(), nullable=False)
    )
    op.create_unique_constraint(
        op.f("uq_book_offers_main_image_id"), "book_offers", ["main_image_id"]
    )
    op.create_foreign_key(
        op.f("fk_book_offers_main_image_id_book_main_images"),
        "book_offers",
        "book_main_images",
        ["main_image_id"],
        ["id"],
        ondelete="SET NULL",
    )
    op.drop_column("book_offers", "main_image_url")


def downgrade() -> None:
    op.add_column(
        "book_offers",
        sa.Column("main_image_url", sa.VARCHAR(), autoincrement=False, nullable=True),
    )
    op.drop_constraint(
        op.f("fk_book_offers_main_image_id_book_main_images"),
        "book_offers",
        type_="foreignkey",
    )
    op.drop_constraint(
        op.f("uq_book_offers_main_image_id"), "book_offers", type_="unique"
    )
    op.drop_column("book_offers", "main_image_id")
    op.drop_table("book_main_images")
