"""empty message

Revision ID: aad7a41b302b
Revises: d2abd49ca007
Create Date: 2025-02-27 22:56:27.621662

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "aad7a41b302b"
down_revision: str | None = "d2abd49ca007"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(op.f("uq_user_id"), "user", ["id"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_user_id"), "user", type_="unique")
