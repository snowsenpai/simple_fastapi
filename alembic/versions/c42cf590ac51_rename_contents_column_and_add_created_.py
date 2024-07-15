"""rename contents column and add created_at and published column

Revision ID: c42cf590ac51
Revises: 3fb3a1d284ef
Create Date: 2024-07-15 18:58:46.542886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c42cf590ac51'
down_revision: Union[str, None] = '3fb3a1d284ef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('posts', 'contents', new_column_name='content')
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                    server_default=sa.text('now()'), nullable=False)
    )
    pass


def downgrade() -> None:
    op.alter_column('posts', 'content', new_column_name='contents')
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
