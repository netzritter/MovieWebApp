"""
Initializer for the models package.

This module defines and exposes the shared SQLAlchemy instance
used throughout the application, and imports the database models
to register them with SQLAlchemy.
"""

from flask_sqlalchemy import SQLAlchemy

# ✅ Shared SQLAlchemy instance, used across the entire app
db = SQLAlchemy()

# Import models to register them with SQLAlchemy
from .models import User, Movie

