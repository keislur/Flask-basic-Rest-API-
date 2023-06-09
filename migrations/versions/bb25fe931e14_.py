"""empty message

Revision ID: bb25fe931e14
Revises: bdd34efc3b25
Create Date: 2023-04-13 13:31:14.265547

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb25fe931e14'
down_revision = 'bdd34efc3b25'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('level', sa.BigInteger(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('level')

    # ### end Alembic commands ###
