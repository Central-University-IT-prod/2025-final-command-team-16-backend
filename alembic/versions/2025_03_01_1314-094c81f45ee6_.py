"""empty message

Revision ID: 094c81f45ee6
Revises: aad7a41b302b
Create Date: 2025-03-01 13:14:32.098732

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "094c81f45ee6"
down_revision: str | None = "aad7a41b302b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "points",
        sa.Column("region", sa.String(length=150), nullable=False),
        sa.Column("city", sa.String(length=150), nullable=False),
        sa.Column("street", sa.String(length=150), nullable=False),
        sa.Column("place", sa.String(length=150), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_points")),
        sa.UniqueConstraint("id", name=op.f("uq_points_id")),
    )


def downgrade() -> None:
    op.drop_table("points")
