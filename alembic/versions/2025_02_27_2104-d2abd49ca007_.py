"""empty message

Revision ID: d2abd49ca007
Revises: 5ad084b4433a
Create Date: 2025-02-27 21:04:39.591788

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d2abd49ca007"
down_revision: str | None = "5ad084b4433a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_user")),
        sa.UniqueConstraint("id", name=op.f("uq_user_id")),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.drop_index("ix_users_username", table_name="users")
    op.drop_table("users")


def downgrade() -> None:
    op.create_table(
        "users",
        sa.Column("username", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("hashed_password", sa.VARCHAR(), autoincrement=False, nullable=False),
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
        sa.PrimaryKeyConstraint("id", name="pk_users"),
        sa.UniqueConstraint("email", name="uq_users_email"),
        sa.UniqueConstraint("id", name="uq_users_id"),
        sa.UniqueConstraint("username", name="uq_users_username"),
    )
    op.create_index(
        "ix_users_username", "users", ["username", "email", "is_active"], unique=False
    )
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
