"""A meme to surpass metal gear

Revision ID: 01c719fe3b1f
Revises: 3eb5fe5f18d4
Create Date: 2021-10-04 03:37:31.995594

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01c719fe3b1f'
down_revision = '3eb5fe5f18d4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('citizens',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('social_credit', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id'], ['members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('citizens')
    # ### end Alembic commands ###
