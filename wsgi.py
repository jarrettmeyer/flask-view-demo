import logging

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Boolean, Column, Integer, MetaData, String, Table

database_uri = 'postgresql://postgres:postgres@localhost:5432/flask-view-demo'

app = Flask('flask-view-demo')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.setLevel(logging.DEBUG)
application = app

db = SQLAlchemy(app)
engine = create_engine(database_uri)
metadata = MetaData()
metadata.bind = engine
migrate = Migrate(app, db)


active_products_view = Table('active_products_view', metadata,
    Column("id", Integer(), primary_key=True),
    Column("name", String(32)),
    autoload=True
)


class ActiveProduct(db.Model):
    __table__ = active_products_view


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(32))
    active = Column(Boolean())


def seed_db():
    count_products = Product.query.count()
    app.logger.debug('count products: %d', count_products)
    if count_products < 5:
        active = False
        for name in ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo']:
            active = not active
            product = Product(name=name, active=active)
            db.session.add(product)
        db.session.commit()
        app.logger.debug('Seeded database.')


def serialize_product(product:Product) -> dict:
    d = {}
    for attr in ['id', 'name', 'active']:
        if hasattr(product, attr):
            d[attr] = getattr(product, attr)
    return d


@app.route('/')
@app.route('/index')
def route_index():
    return ('Hello, World!', 200)


@app.route('/products')
def route_products():
    products = Product.query.all()
    products_dict = [serialize_product(product) for product in products]
    return jsonify(products_dict)


@app.route('/products/active')
def route_products_active():
    products = ActiveProduct.query.all()
    products_dict = [serialize_product(product) for product in products]
    return jsonify(products_dict)


if __name__ == '__main__':
    seed_db()
    app.run(
        debug=True
    )
