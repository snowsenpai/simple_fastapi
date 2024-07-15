"""add users table

Revision ID: 276309ea9213
Revises: 7a77ea1ac628
Create Date: 2024-07-15 17:12:30.318850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '276309ea9213'
down_revision: Union[str, None] = '7a77ea1ac628'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users', 
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('email', sa.String, nullable=False, unique=True),
                    sa.Column('password', sa.String, nullable=False), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False)
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
