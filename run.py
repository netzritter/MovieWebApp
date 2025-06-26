from movie_web_app import create_app
from movie_web_app.models import db

# Create the Flask app using the app factory
app = create_app()

if __name__ == "__main__":
    # Push the app context to create DB tables
    with app.app_context():
        db.create_all()  # Create all tables if they don't exist

    # Run the app on 0.0.0.0 and port 5000 for Codio compatibility
    app.run(host='0.0.0.0', port=5000, debug=True)
