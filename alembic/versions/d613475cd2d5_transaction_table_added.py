"""transaction table added

Revision ID: d613475cd2d5
Revises: e635b077322e
Create Date: 2023-03-29 17:02:28.207439

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd613475cd2d5'
down_revision = 'e635b077322e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('transaction',
    sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('balance', sa.Integer(), nullable=True),
    sa.Column('amount_added', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('channel', sa.String(length=200), nullable=True),
    sa.Column('gateway_response', sa.String(length=200), nullable=True),
    sa.Column('created_at', sa.Time(), nullable=True),
    sa.Column('paid_at', sa.Time(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    # ### end Alembic commands ###
