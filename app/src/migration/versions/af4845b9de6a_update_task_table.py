"""update task table

Revision ID: af4845b9de6a
Revises: 794fc0a0c5b0
Create Date: 2024-07-20 15:41:37.930285

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'af4845b9de6a'
down_revision: Union[str, None] = '794fc0a0c5b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('create_user_id', sa.Integer(), nullable=False))
    op.drop_constraint('task_ibfk_1', 'task', type_='foreignkey')
    op.create_foreign_key(None, 'task', 'user', ['create_user_id'], ['id'])
    op.drop_column('task', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('task', sa.Column('user_id', mysql.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.create_foreign_key('task_ibfk_1', 'task', 'user', ['user_id'], ['id'])
    op.drop_column('task', 'create_user_id')
    # ### end Alembic commands ###
