"""empty message

Revision ID: d38d78a36637
Revises: e69706ab295a
Create Date: 2022-06-01 05:14:29.938006

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd38d78a36637'
down_revision = 'e69706ab295a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('website', sa.String(length=150), nullable=True))
    op.add_column('Venue', sa.Column('seeking_talent', sa.Boolean(), nullable=True))
    op.add_column('Venue', sa.Column('seeking_description', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Venue', 'seeking_description')
    op.drop_column('Venue', 'seeking_talent')
    op.drop_column('Venue', 'website')
    # ### end Alembic commands ###