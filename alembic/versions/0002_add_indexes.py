"""add indexes

Revision ID: 0002
Revises: 22eb6f0391f3
Create Date: 2026-03-02 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = '0002'
down_revision: Union[str, None] = '22eb6f0391f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_posts_owner_id', 'posts', ['owner_id'])


def downgrade() -> None:
    op.drop_index('ix_posts_owner_id', table_name='posts')
