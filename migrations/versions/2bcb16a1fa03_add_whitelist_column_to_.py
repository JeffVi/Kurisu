"""Add whitelist column to levenshteinwords table

Revision ID: 2bcb16a1fa03
Revises: dc5f272ffa13
Create Date: 2021-08-13 18:50:19.166588

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bcb16a1fa03'
down_revision = 'dc5f272ffa13'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('levenshteinwords', sa.Column('whitelist', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('levenshteinwords', 'whitelist')
    # ### end Alembic commands ###
