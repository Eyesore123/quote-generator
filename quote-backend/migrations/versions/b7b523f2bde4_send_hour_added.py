"""send_hour added

Revision ID: b7b523f2bde4
Revises: 3884d31765c4
Create Date: 2025-04-25 16:27:28.312156

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7b523f2bde4'
down_revision = '3884d31765c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('subscriber', sa.Column('send_hour', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subscriber', 'send_hour')
    # ### end Alembic commands ###
