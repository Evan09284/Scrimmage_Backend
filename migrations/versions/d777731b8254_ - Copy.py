"""empty message

Revision ID: d777731b8254
Revises: 74aecea38558
Create Date: 2021-10-05 14:22:38.208787

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd777731b8254'
down_revision = '74aecea38558'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('users_author_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'author_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('author_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('users_author_id_fkey', 'users', 'authors', ['author_id'], ['id'])
    # ### end Alembic commands ###