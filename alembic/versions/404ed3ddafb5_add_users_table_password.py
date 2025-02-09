"""add users table password

Revision ID: 404ed3ddafb5
Revises: b06e8e7530b5
Create Date: 2025-02-09 15:29:49.467942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '404ed3ddafb5'
down_revision: Union[str, None] = 'b06e8e7530b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'hashed_password')
    # ### end Alembic commands ###
