"""modifying customer model

Revision ID: dbbbde53ecb8
Revises: 384e027c158e
Create Date: 2021-11-08 18:20:36.347307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbbbde53ecb8'
down_revision = '384e027c158e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('phone', sa.String(), nullable=True))
    op.drop_column('customer', 'phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('customer', sa.Column('phone_number', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('customer', 'phone')
    # ### end Alembic commands ###