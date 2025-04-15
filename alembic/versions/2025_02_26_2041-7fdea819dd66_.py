"""empty message

Revision ID: 7fdea819dd66
Revises: adeed025f926
Create Date: 2025-02-26 20:41:00.712285

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7fdea819dd66"
down_revision: str | None = "adeed025f926"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "tokens",
        sa.Column("token", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_tokens_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_tokens")),
        sa.UniqueConstraint("id", name=op.f("uq_tokens_id")),
    )
    op.create_index(
        op.f("ix_tokens_token"),
        "tokens",
        ["token", "expires_at", "user_id"],
        unique=False,
    )
    op.create_unique_constraint(op.f("uq_users_id"), "users", ["id"])


def downgrade() -> None:
    op.drop_constraint(op.f("uq_users_id"), "users", type_="unique")
    op.drop_index(op.f("ix_tokens_token"), table_name="tokens")
    op.drop_table("tokens")
