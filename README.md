# Flask View Demo

A super simple Python Flask application with views, reflections, and migrations.

The migration to create the view looks like the following code block (see [8233f2f356f1](/jarrettmeyer/flask-view-demo/blob/master/migrations/versions/78372dd6be7b_create_active_products_view.py)).

```py
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
```

Alternatively, you could keep the SQL in a file.

```py
def upgrade():
    connection = op.get_bind()
    with open('/path/to/create_view.psql', 'r') as file:
        result = connection.execute(file.read())
        file.close()

def downgrade():
    connection = op.get_bind()
    with open('/path/to/drop_view.psql', 'r') as file:
        result = connection.execute(file.read())
        file.close()
```

Once the view is defined, we can reflect our view with the following code (see [db.py](/jarrettmeyer/flask-view-demo/blob/master/flask_view_demo/db.py)).

```py
class ActiveProduct(Product):
    __tablename__ = 'active_products'
```


