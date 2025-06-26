from sqlalchemy.exc import SQLAlchemyError
from movie_web_app.models.models import db, User, Movie
from datamanager.data_manager_interface import DataManagerInterface

class SQLiteDataManager(DataManagerInterface):
    """
    SQLiteDataManager implements DataManagerInterface and handles
    all interactions with the SQLite database for users and movies.
    """

    def get_all_users(self):
        """Retrieve all users from the database."""
        try:
            return User.query.all()
        except SQLAlchemyError as e:
            print(f"[SQLiteDataManager] Error retrieving users: {e}")
            return []

    def get_user(self, user_id):
        """Retrieve a single user by ID."""
        try:
            return User.query.get(user_id)
        except SQLAlchemyError as e:
            print(f"[SQLiteDataManager] Error retrieving user {user_id}: {e}")
            return None

    def get_user_movies(self, user_id):
        """Retrieve all movies for a given user."""
        try:
            user = User.query.get(user_id)
            if user:
                return user.movies
            print(f"[SQLiteDataManager] No user found with ID {user_id}")
            return []
        except SQLAlchemyError as e:
            print(f"[SQLiteDataManager] Error retrieving movies for user {user_id}: {e}")
            return []

    def add_user(self, name):
        """Add a new user to the database."""
        try:
            user = User(name=name)
            db.session.add(user)
            db.session.commit()
            print(f"[SQLiteDataManager] Added user: {user.name} (ID: {user.id})")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[SQLiteDataManager] Error adding user: {e}")

    def add_movie(self, user_id, movie_data):
        """Add a new movie to a specific user."""
        try:
            user = User.query.get(user_id)
            if not user:
                print(f"[SQLiteDataManager] User ID {user_id} not found. Movie not added.")
                return

            movie = Movie(
                name=movie_data['name'],
                director=movie_data['director'],
                year=movie_data['year'],
                rating=movie_data['rating'],
                user=user
            )
            db.session.add(movie)
            db.session.commit()
            print(f"[SQLiteDataManager] Added movie '{movie.name}' for user ID {user_id}")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[SQLiteDataManager] Error adding movie: {e}")

    def update_movie(self, movie_id, updated_data):
        """Update an existing movie's information."""
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                print(f"[SQLiteDataManager] Movie ID {movie_id} not found. Update skipped.")
                return

            movie.name = updated_data['name']
            movie.director = updated_data['director']
            movie.year = updated_data['year']
            movie.rating = updated_data['rating']
            db.session.commit()
            print(f"[SQLiteDataManager] Updated movie ID {movie_id}")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[SQLiteDataManager] Error updating movie: {e}")

    def delete_movie(self, movie_id):
        """Delete a movie by its ID."""
        try:
            movie = Movie.query.get(movie_id)
            if not movie:
                print(f"[SQLiteDataManager] Movie ID {movie_id} not found. Delete skipped.")
                return

            db.session.delete(movie)
            db.session.commit()
            print(f"[SQLiteDataManager] Deleted movie ID {movie_id}")
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[SQLiteDataManager] Error deleting movie: {e}")

# Singleton instance
_data_manager = SQLiteDataManager()

def get_data_manager():
    """
    Get the shared singleton instance of the SQLiteDataManager.
    This ensures consistent database access across the app.
    """
    return _data_manager
