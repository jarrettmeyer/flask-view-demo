import logging
import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData

app = Flask('flask-view-demo')
app.logger.setLevel(logging.DEBUG)
app.template_folder = '{0}/flask_view_demo/templates'.format(os.getcwd())

# Set the database URI.
database_uri = os.getenv('DATABASE_URI', 'postgresql://postgres:postgres@localhost:5432/flask-view-demo')

# Define the db engine and metadata.
engine = create_engine(database_uri)
metadata = MetaData()
metadata.bind = engine

# Update the app configuration and define the database.
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the migration engine.
migrate = Migrate(app, db)

import flask_view_demo.db
import flask_view_demo.routes
