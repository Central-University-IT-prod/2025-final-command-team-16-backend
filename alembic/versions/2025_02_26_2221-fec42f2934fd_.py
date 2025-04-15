"""empty message

Revision ID: fec42f2934fd
Revises: 18bc3035b00f
Create Date: 2025-02-26 22:21:14.952146

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "fec42f2934fd"
down_revision: str | None = "18bc3035b00f"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint(op.f("uq_refresh_tokens_id"), "refresh_tokens", ["id"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_refresh_tokens_id"), "refresh_tokens", type_="unique")
