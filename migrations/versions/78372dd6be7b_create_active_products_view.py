"""create active_products view

Revision ID: 78372dd6be7b
Revises: 8233f2f356f1
Create Date: 2019-06-15 15:36:29.763219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78372dd6be7b'
down_revision = '8233f2f356f1'
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    result = connection.execute("""
    CREATE OR REPLACE VIEW active_products AS
        SELECT id, name, active
        FROM products
        WHERE active = true
    """)


def downgrade():
    connection = op.get_bind()
    result = connection.execute('DROP VIEW active_products')
