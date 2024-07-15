"""add content column to posts table

Revision ID: 7a77ea1ac628
Revises: 40eeb4aadacf
Create Date: 2024-07-15 14:56:57.826494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a77ea1ac628'
down_revision: Union[str, None] = '40eeb4aadacf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('contents', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'contents')
    pass
