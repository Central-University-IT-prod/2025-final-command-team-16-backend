"""empty message

Revision ID: 18bc3035b00f
Revises: 7fdea819dd66
Create Date: 2025-02-26 21:35:45.513587

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "18bc3035b00f"
down_revision: str | None = "7fdea819dd66"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index("ix_tokens_token", table_name="tokens")
    op.rename_table("tokens", "refresh_tokens")
    op.create_index(
        op.f("ix_refresh_tokens_token"),
        "refresh_tokens",
        ["token", "expires_at", "user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_refresh_tokens_token"), table_name="refresh_tokens")
    op.rename_table("refresh_tokens", "tokens")
    op.create_index(
        "ix_tokens_token", "tokens", ["token", "expires_at", "user_id"], unique=False
    )
