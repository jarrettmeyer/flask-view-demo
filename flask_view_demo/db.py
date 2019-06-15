"""
Functions for working with the database.
"""
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Boolean, Column, Integer, MetaData, String, Table
from typing import List

from flask_view_demo import db, metadata
from flask_view_demo.alphabet import alphabet


class ActiveProduct(db.Model):
    __table__ = Table('active_products_view', metadata,
        Column("id", Integer(), primary_key=True),
        Column("name", String(32)),
        Column("active", Boolean()),
        autoload=True,
    )


class Product(db.Model):
    __tablename__ = 'products'
    id = Column(Integer(), nullable=False, primary_key=True)
    name = Column(String(32))
    active = Column(Boolean())


def get_all_active_products() -> List[ActiveProduct]:
    products = ActiveProduct.query.all()
    return products


def get_all_products() -> List[Product]:
    products = Product.query.all()
    return products


def get_product(name:str) -> Product:
    product = Product.query.filter(Product.name == name).first()
    return product


def seed_db():
    Product.query.delete()
    db.session.commit()

    active = False
    for letter in alphabet:
        active = not active
        product = Product(name=letter, active=active)
        db.session.add(product)

    db.session.commit()

    count_products = Product.query.count()
    app.logger.debug('Seeded products table with %d rows.', count_products)


def serialize_product(product:Product) -> dict:
    d = {}
    for attr in ['id', 'name', 'active']:
        if hasattr(product, attr):
            d[attr] = getattr(product, attr)
    return d
