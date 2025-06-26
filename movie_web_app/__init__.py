import os
from flask import Flask
from movie_web_app.models import db  # Shared SQLAlchemy instance
from movie_web_app.routes import register_routes  # Routes registration function


def create_app():
    """
    Factory function to create and configure the Flask app instance.

    Returns:
        Flask app object
    """
    app = Flask(__name__)

    # Configure SQLite database
    basedir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(basedir, '..', 'datamanager', 'movieweb.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database connection with this app
    db.init_app(app)

    # Register application routes
    register_routes(app)

    return app
