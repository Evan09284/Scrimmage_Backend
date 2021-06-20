"""empty message

Revision ID: 2f744386111a
Revises: 517b5ea34274
Create Date: 2021-10-24 14:27:26.170436

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '2f744386111a'
down_revision = '517b5ea34274'
branch_labels = None
depends_on = None


def upgrade():
    notification_status = postgresql.ENUM('inactive', 'scheduled', 'notified',
                                          name='notificationstatusenum')
    notification_status.create(op.get_bind())

    op.add_column('user_bets', sa.Column('notification_status', postgresql.ARRAY(
        postgresql.ENUM('inactive', 'scheduled', 'notified', name='notificationstatusenum')),
                                         nullable=True, server_default='{notified}'))


def downgrade():
    op.drop_column('user_bets', 'notification_status')

    notification_status = postgresql.ENUM('inactive', 'scheduled', 'notified',
                                          name='notificationstatusenum')
    notification_status.drop(op.get_bind())
