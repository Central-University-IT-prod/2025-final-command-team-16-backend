"""empty message

Revision ID: 5ad084b4433a
Revises: fec42f2934fd
Create Date: 2025-02-27 20:35:24.118226

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5ad084b4433a"
down_revision: str | None = "fec42f2934fd"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.drop_index("ix_refresh_tokens_token", table_name="refresh_tokens")
    op.drop_table("refresh_tokens")


def downgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("token", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "expires_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=False
        ),
        sa.Column("user_id", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("is_active", sa.BOOLEAN(), autoincrement=False, nullable=False),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "updated_at", postgresql.TIMESTAMP(), autoincrement=False, nullable=True
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name="fk_tokens_user_id_users",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_tokens"),
        sa.UniqueConstraint("id", name="uq_refresh_tokens_id"),
    )
    op.create_index(
        "ix_refresh_tokens_token",
        "refresh_tokens",
        ["token", "expires_at", "user_id"],
        unique=False,
    )
