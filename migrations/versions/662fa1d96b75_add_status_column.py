"""add status column

Revision ID: 662fa1d96b75
Revises: 4e081b9cb43a
Create Date: 2024-02-19 11:57:51.157947

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '662fa1d96b75'
down_revision = '4e081b9cb43a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hiredcars', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('hiredcars', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
