"""notifications

Revision ID: 1720bc2ce1b5
Revises: 
Create Date: 2018-07-04 16:18:07.055041

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1720bc2ce1b5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notification',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.Float(), nullable=True),
    sa.Column('payload_json', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_name'), 'notification', ['name'], unique=False)
    op.create_index(op.f('ix_notification_timestamp'), 'notification', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_notification_timestamp'), table_name='notification')
    op.drop_index(op.f('ix_notification_name'), table_name='notification')
    op.drop_table('notification')
    # ### end Alembic commands ###
