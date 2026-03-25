"""Create phone number for user column

Revision ID: f51eb13eb540
Revises: 
Create Date: 2026-03-25 17:39:21.898412

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f51eb13eb540'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    #codigo para agregar una nueva columna a la tabla users 
    # llamada phone_number de tipo string y que permita valores nulos
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
