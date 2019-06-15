import logging

from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, Integer, String


app = Flask('flask-view-demo')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/flask-view-demo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.setLevel(logging.DEBUG)
application = app

db = SQLAlchemy(app)
migrate = Migrate(app, db)


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
    return {
        'id': product.id,
        'name': product.name,
        'active': product.active
    }


@app.route('/')
@app.route('/index')
def route_index():
    return ('Hello, World!', 200)


@app.route('/products')
def route_product():
    products = Product.query.all()
    products_dict = [serialize_product(product) for product in products]
    return jsonify(products_dict)


if __name__ == '__main__':
    seed_db()
    app.run(
        debug=True
    )
