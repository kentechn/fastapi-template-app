"""create user table

Revision ID: 794fc0a0c5b0
Revises: 40661a7034ad
Create Date: 2024-07-20 15:26:15.362548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '794fc0a0c5b0'
down_revision: Union[str, None] = '40661a7034ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False, comment='ユーザーID'),
    sa.Column('is_admin', sa.Boolean(), nullable=False, comment='管理者権限'),
    sa.Column('username', sa.String(length=255), nullable=False, comment='ユーザー名'),
    sa.Column('hashed_password', sa.String(length=255), nullable=False, comment='ハッシュ化パスワード'),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False, comment='作成日時'),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False, comment='更新日時'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('task', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'task', 'user', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'task', type_='foreignkey')
    op.drop_column('task', 'user_id')
    op.drop_table('user')
    # ### end Alembic commands ###