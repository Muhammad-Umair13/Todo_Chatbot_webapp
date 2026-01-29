"""Initial task table

Revision ID: 001_initial_task
Revises:
Create Date: 2026-01-14 12:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial_task'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the task table
    op.create_table('task',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False, default=""),
        sa.Column('completed', sa.Boolean(), nullable=False, default=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create indexes
    op.create_index('ix_task_user_id', 'task', ['user_id'])
    op.create_index('ix_task_user_id_completed', 'task', ['user_id', 'completed'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('ix_task_user_id_completed', table_name='task')
    op.drop_index('ix_task_user_id', table_name='task')

    # Drop table
    op.drop_table('task')