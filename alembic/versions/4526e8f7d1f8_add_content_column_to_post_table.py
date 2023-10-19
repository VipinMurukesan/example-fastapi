"""add content column to post table

Revision ID: 4526e8f7d1f8
Revises: 555a626b2f44
Create Date: 2023-10-19 11:07:53.076868

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4526e8f7d1f8"
down_revision: Union[str, None] = "555a626b2f44"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("post", "content")
