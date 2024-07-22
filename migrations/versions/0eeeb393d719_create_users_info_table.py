"""create users_info table

Revision ID: 0eeeb393d719
Revises: 
Create Date: 2024-07-22 19:08:45.101764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0eeeb393d719'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table('users_info',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('gender', sa.String(length=50), nullable=False),
        sa.Column('phone_number', sa.String(length=20), nullable=False),
        sa.Column('weight', sa.Float(), nullable=True),
        sa.Column('height', sa.Float(), nullable=True),
        sa.Column('age', sa.Integer(), nullable=False),
        sa.Column('bmi', sa.Float(), nullable=True),
        sa.Column('emergency_contact_number', sa.String(length=20), nullable=True),
        sa.ForeignKeyConstraint(['id'], ['users.id'], ),  # Adding the foreign key constraint
        sa.PrimaryKeyConstraint('id')  # Defining the primary key
    )

def downgrade():
    op.drop_table('users_info')