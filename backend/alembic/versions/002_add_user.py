"""Add user table

Revision ID: 002_add_user
Revises: 001_initial_task
Create Date: 2026-01-15 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision: str = '002_add_user'
down_revision: str = '001_initial_task'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the user table
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
        sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )

    # Create indexes
    op.create_index('ix_user_email', 'user', ['email'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_user_email', table_name='user')

    # Drop table
    op.drop_table('user')
