"""creates rental model

Revision ID: 815a812e8bbc
Revises: dbbbde53ecb8
Create Date: 2021-11-10 13:20:13.518080

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '815a812e8bbc'
down_revision = 'dbbbde53ecb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rental', sa.Column('customer_id', sa.Integer(), nullable=False))
    op.add_column('rental', sa.Column('video_id', sa.Integer(), nullable=False))
    op.add_column('rental', sa.Column('videos_checked_out_count', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'rental', 'video', ['video_id'], ['video_id'])
    op.create_foreign_key(None, 'rental', 'customer', ['customer_id'], ['id'])
    op.drop_column('rental', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rental', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.drop_constraint(None, 'rental', type_='foreignkey')
    op.drop_constraint(None, 'rental', type_='foreignkey')
    op.drop_column('rental', 'videos_checked_out_count')
    op.drop_column('rental', 'video_id')
    op.drop_column('rental', 'customer_id')
    # ### end Alembic commands ###
