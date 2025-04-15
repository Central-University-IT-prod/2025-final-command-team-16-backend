"""empty message

Revision ID: 99986514d6a8
Revises: fd35f778c495
Create Date: 2025-03-02 09:28:10.921961

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "99986514d6a8"
down_revision: str | None = "fd35f778c495"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_column("points", "street")
    op.drop_column("points", "region")


def downgrade() -> None:
    op.add_column(
        "points",
        sa.Column(
            "region", sa.VARCHAR(length=150), autoincrement=False, nullable=False
        ),
    )
    op.add_column(
        "points",
        sa.Column(
            "street", sa.VARCHAR(length=150), autoincrement=False, nullable=False
        ),
    )
