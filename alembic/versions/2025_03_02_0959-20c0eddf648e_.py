"""empty message

Revision ID: 20c0eddf648e
Revises: 99986514d6a8
Create Date: 2025-03-02 09:59:36.738364

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "20c0eddf648e"
down_revision: str | None = "99986514d6a8"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("book_offers", "publisher_name", new_column_name="publisher")
    op.alter_column("book_offers", "physical_state", new_column_name="condition")
    op.alter_column("book_offers", "pages_number", new_column_name="pages_count")
    op.add_column("book_offers", sa.Column("year", sa.Integer(), nullable=False))


def downgrade() -> None:
    op.alter_column("book_offers", "pages_count", new_column_name="pages_number")
    op.alter_column("book_offers", "condition", new_column_name="physical_state")
    op.alter_column("book_offers", "publisher", new_column_name="publisher_name")
    op.drop_column("book_offers", "year")
