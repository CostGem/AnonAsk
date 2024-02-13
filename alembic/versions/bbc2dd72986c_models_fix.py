"""Models fix

Revision ID: bbc2dd72986c
Revises: 0ff9b5822dc8
Create Date: 2024-01-14 15:24:07.655133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbc2dd72986c'
down_revision = '0ff9b5822dc8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('commented_at', sa.DateTime(), nullable=False))
    op.alter_column('comments', 'message_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('comments', 'message_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.drop_column('comments', 'commented_at')
    # ### end Alembic commands ###