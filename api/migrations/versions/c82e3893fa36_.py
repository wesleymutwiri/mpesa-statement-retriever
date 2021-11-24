"""empty message

Revision ID: c82e3893fa36
Revises: ae096bbf0941
Create Date: 2021-11-09 17:42:36.559611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c82e3893fa36'
down_revision = 'ae096bbf0941'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('goals', sa.Column('current_price', sa.Integer(), nullable=True))
    op.add_column('goals', sa.Column('is_completed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('goals', 'is_completed')
    op.drop_column('goals', 'current_price')
    # ### end Alembic commands ###