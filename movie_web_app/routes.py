from flask import render_template, request, redirect
from datamanager.sqlite_data_manager import get_data_manager
from omdb_api import fetch_movie_data

# Singleton data manager instance
data_manager = get_data_manager()

def register_routes(app):
    """
    Register all Flask routes to the app instance.

    Args:
        app (Flask): The Flask app to register routes to.
    """

    @app.route('/')
    def home():
        """Render the home page."""
        return render_template('home.html')

    @app.route('/users')
    def user_list():
        """Display a list of all users."""
        all_users = data_manager.get_all_users()
        return render_template('user_list.html', users={u.id: u for u in all_users})

    @app.route('/users/<int:user_id>')
    def user_movies(user_id):
        """
        Show all movies belonging to a specific user.

        Args:
            user_id (int): ID of the user.
        """
        user = data_manager.get_user(user_id)
        if user:
            return render_template('user_movies.html', user=user, user_id=user_id)
        return "User not found", 404

    @app.route('/add_user', methods=['GET', 'POST'])
    def add_user():
        """Add a new user via form submission."""
        if request.method == 'POST':
            name = request.form['name']
            data_manager.add_user(name)
            return redirect('/users')
        return render_template('add_user.html')

    @app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
    def add_movie(user_id):
        """
        Add a new movie to a specific user.

        Args:
            user_id (int): ID of the user.
        """
        user = data_manager.get_user(user_id)
        if not user:
            return "User not found", 404

        if request.method == 'POST':
            title_input = request.form['name']
            omdb_data = fetch_movie_data(title_input)

            movie_data = {
                'name': request.form.get('name') or omdb_data.get('name'),
                'director': request.form.get('director') or omdb_data.get('director'),
                'year': int(request.form.get('year') or omdb_data.get('year') or 0),
                'rating': float(request.form.get('rating') or omdb_data.get('rating') or 0.0)
            }

            data_manager.add_movie(user_id, movie_data)
            return redirect(f'/users/{user_id}')

        return render_template('add_movie.html', user=user, user_id=user_id)

    @app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
    def update_movie(user_id, movie_id):
        """
        Update an existing movie for a user.

        Args:
            user_id (int): ID of the user.
            movie_id (int): ID of the movie.
        """
        user = data_manager.get_user(user_id)
        if not user:
            return "User not found", 404

        movie = next((m for m in user.movies if m.id == movie_id), None)
        if not movie:
            return "Movie not found", 404

        if request.method == 'POST':
            updated_data = {
                'name': request.form['name'],
                'director': request.form['director'],
                'year': int(request.form['year']),
                'rating': float(request.form['rating'])
            }
            data_manager.update_movie(movie_id, updated_data)
            return redirect(f'/users/{user_id}')

        return render_template('update_movie.html', movie=movie, user_id=user_id)

    @app.route('/users/<int:user_id>/delete_movie/<int:movie_id>')
    def delete_movie(user_id, movie_id):
        """
        Delete a movie associated with a user.

        Args:
            user_id (int): ID of the user.
            movie_id (int): ID of the movie.
        """
        user = data_manager.get_user(user_id)
        if not user:
            return "User not found", 404

        data_manager.delete_movie(movie_id)
        return redirect(f'/users/{user_id}')

    @app.errorhandler(404)
    def page_not_found(_):
        """Render custom 404 Not Found page."""
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(_):
        """Render custom 500 Internal Server Error page."""
        return render_template('500.html'), 500
