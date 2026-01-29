"""Add Conversation and Message tables for Phase III AI Chatbot

Revision ID: 003_add_chat_models
Revises: 002_add_user
Create Date: 2026-01-24 12:00:00.000000

Phase III: AI Chatbot - Chat history persistence
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

# revision identifiers, used by Alembic.
revision: str = '003_add_chat_models'
down_revision: str = '002_add_user'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the conversation table
    op.create_table('conversation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create indexes for conversation
    op.create_index('ix_conversation_user_id', 'conversation', ['user_id'])
    op.create_index('ix_conversation_user_id_created_at', 'conversation', ['user_id', 'created_at'])

    # Create the message table
    op.create_table('message',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('role', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('extra_data', sa.JSON(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversation.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )

    # Create indexes for message
    op.create_index('ix_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('ix_message_conversation_id_created_at', 'message', ['conversation_id', 'created_at'])


def downgrade() -> None:
    # Drop indexes for message
    op.drop_index('ix_message_conversation_id_created_at', table_name='message')
    op.drop_index('ix_message_conversation_id', table_name='message')

    # Drop message table
    op.drop_table('message')

    # Drop indexes for conversation
    op.drop_index('ix_conversation_user_id_created_at', table_name='conversation')
    op.drop_index('ix_conversation_user_id', table_name='conversation')

    # Drop conversation table
    op.drop_table('conversation')
