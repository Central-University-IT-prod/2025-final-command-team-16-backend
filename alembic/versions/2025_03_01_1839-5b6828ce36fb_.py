"""empty message

Revision ID: 5b6828ce36fb
Revises: cb3a98e6139a
Create Date: 2025-03-01 18:39:26.040120

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5b6828ce36fb"
down_revision: str | None = "cb3a98e6139a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(op.f("uq_book_offers_id"), "book_offers", ["id"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_book_offers_id"), "book_offers", type_="unique")
