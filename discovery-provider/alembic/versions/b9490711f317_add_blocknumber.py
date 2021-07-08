"""Add blocknumber

Revision ID: b9490711f317
Revises: 6bd5882912c8
Create Date: 2018-12-07 10:48:06.741940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "b9490711f317"
down_revision = "2571ec7593c7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("blocks", sa.Column("number", sa.Integer(), nullable=True))
    op.add_column("tracks", sa.Column("blocknumber", sa.Integer(), nullable=True))
    op.add_column("users", sa.Column("blocknumber", sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("users", "blocknumber")
    op.drop_column("tracks", "blocknumber")
    op.drop_column("blocks", "number")
    # ### end Alembic commands ###
