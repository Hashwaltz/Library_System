"""added in out status to entry log

Revision ID: 52941112e48a
Revises: 36c80a02dae1
Create Date: 2026-02-16 09:21:02.887410
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '52941112e48a'
down_revision = '36c80a02dae1'
branch_labels = None
depends_on = None


def upgrade():
    # Add status column WITH DEFAULT for SQLite
    with op.batch_alter_table('entry_log', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'status',
                sa.String(length=3),
                nullable=False,
                server_default='IN'
            )
        )


def downgrade():
    with op.batch_alter_table('entry_log', schema=None) as batch_op:
        batch_op.drop_column('status')
