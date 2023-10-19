"""Add foreign key to post table

Revision ID: dd5204942388
Revises: 33d66aa19f09
Create Date: 2023-10-19 11:20:22.869027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dd5204942388"
down_revision: Union[str, None] = "33d66aa19f09"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("post", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_user_fk",
        source_table="post",
        referent_table="user",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("post_user_fk", table_name="post")
    op.drop_column("post", "owner_id")
