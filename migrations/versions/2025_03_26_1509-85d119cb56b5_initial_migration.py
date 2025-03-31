"""Initial migration

Revision ID: 85d119cb56b5
Revises: 
Create Date: 2025-03-26 15:09:06.229383

"""
from alembic import op
import sqlalchemy as sa


revision = '85d119cb56b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('questions',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), autoincrement=True, nullable=False),
    sa.Column('text', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('answers',
    sa.Column('id', sa.Integer(), sa.Identity(always=True), autoincrement=True, nullable=False),
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('is_agree', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statistics',
    sa.Column('question_id', sa.Integer(), nullable=False),
    sa.Column('agree_count', sa.Integer(), nullable=False),
    sa.Column('disagree_count', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['question_id'], ['questions.id'], ),
    sa.PrimaryKeyConstraint('question_id')
    )


def downgrade():
    op.drop_table('statistics')
    op.drop_table('answers')
    op.drop_table('questions')
