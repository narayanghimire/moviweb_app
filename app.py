import os

from dotenv import load_dotenv
from flask import Flask, render_template

from app.controller.users_movie_controller import users_movie_controller
from app.services.movie_service import MovieService
from logger.logger import setup_logger


# Set up the logger for this module
logger = setup_logger(__name__)

# Create Flask app
app = Flask(__name__)

# Register Blueprints
app.register_blueprint(users_movie_controller)

load_dotenv()
DB_NAME = os.getenv('DB_NAME', 'moviwebapp.dbb')
if not DB_NAME:
    raise Exception("Movie DB Key not found in environment variables.")
movie_service = MovieService(DB_NAME)

# Route: Home Page
@app.route('/')
def home():
    users = movie_service.get_all_users()
    total_users = len(users)
    total_movies = sum(user["movies_count"] for user in users)
    user_favorites = movie_service.data_manager.get_user_favorites()

    app.logger.info("Rendered the home page successfully.")
    last_5_users = users[-6:]

    return render_template(
        "index.html",
        total_users=total_users,
        total_movies=total_movies,
        user_favorites=user_favorites,
        users=last_5_users,
    )

@app.errorhandler(404)
def page_not_found(e):
    """Displaying message if any http route i not found  """
    app.logger.warning("Page not found: 404.")
    return render_template('404.html'), 404

@app.errorhandler(Exception)
def handle_error(e):
    """Global error handler for all exceptions."""
    app.logger.error(f"An unhandled exception occurred: {e}", exc_info=True)
    return render_template('error.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
