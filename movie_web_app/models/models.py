"""
Database model definitions for the Movie Web App.

Includes:
- User: represents a user who can add movies
- Movie: represents a movie added by a user
"""

from movie_web_app.models import db  # ✅ Use shared SQLAlchemy instance


class User(db.Model):
    """
    Represents a user in the system.
    A user can have many movies.
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    movies = db.relationship(
        'Movie',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    def __repr__(self):
        return f"<User {self.id} - {self.name}>"


class Movie(db.Model):
    """
    Represents a movie added by a user.
    Each movie belongs to a single user.
    """
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    director = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', back_populates='movies')

    def __repr__(self):
        return f"<Movie {self.id} - {self.name}>"
