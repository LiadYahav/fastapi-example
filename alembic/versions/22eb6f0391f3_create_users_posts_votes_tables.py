"""create tables

Revision ID: 22eb6f0391f3
Revises:
Create Date: 2026-03-02 12:51:54.937018

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22eb6f0391f3'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )

    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
    )

    op.create_table(
        'votes',
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, nullable=False),
        sa.Column('post_id', sa.Integer(), sa.ForeignKey('posts.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('votes')
    op.drop_table('posts')
    op.drop_table('users')
