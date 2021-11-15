"""modifies rental model

Revision ID: e19dc75137e3
Revises: e95cbb86183b
Create Date: 2021-11-15 13:01:12.534987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e19dc75137e3'
down_revision = 'e95cbb86183b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rental', sa.Column('checked_in', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rental', 'checked_in')
    # ### end Alembic commands ###