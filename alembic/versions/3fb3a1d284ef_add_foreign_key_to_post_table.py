"""add foreign key to post table

Revision ID: 3fb3a1d284ef
Revises: 276309ea9213
Create Date: 2024-07-15 18:31:39.336556

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fb3a1d284ef'
down_revision: Union[str, None] = '276309ea9213'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))

    op.create_foreign_key('post_users_id', source_table='posts', referent_table='users',
     local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_id', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
