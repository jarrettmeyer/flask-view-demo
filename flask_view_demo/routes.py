from flask import jsonify, render_template

from flask_view_demo import app
from flask_view_demo.db import *

@app.route('/')
@app.route('/index')
def route_index():
    return render_template('index.html')


@app.route('/products')
def route_products():
    products = get_all_products()
    products_dict = [serialize_product(product) for product in products]
    return jsonify(products_dict)


@app.route('/products/active')
def route_products_active():
    products = get_all_active_products()
    products_dict = [serialize_product(product) for product in products]
    return jsonify(products_dict)
