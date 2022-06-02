"""empty message

Revision ID: d8fac4500909
Revises: 3cd9c87df92e
Create Date: 2022-06-02 05:50:02.187043

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8fac4500909'
down_revision = '3cd9c87df92e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('city', sa.String(), nullable=True))
    op.add_column('Venue', sa.Column('state', sa.String(), nullable=True))
    op.drop_constraint('Venue_city_id_fkey', 'Venue', type_='foreignkey')
    op.drop_column('Venue', 'city_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('city_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('Venue_city_id_fkey', 'Venue', 'City', ['city_id'], ['id'])
    op.drop_column('Venue', 'state')
    op.drop_column('Venue', 'city')
    # ### end Alembic commands ###
