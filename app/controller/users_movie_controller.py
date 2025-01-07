import logging
import os
from xml.dom import NotFoundErr

from flask import Blueprint, render_template, request, redirect, jsonify, url_for
from app.services.movie_service import MovieService
from werkzeug.exceptions import BadRequest
from dotenv import load_dotenv
from app.validation.movie_validator import MovieValidator
from app.validation.user_validator import UserValidator

load_dotenv()
users_movie_controller = Blueprint('users_movie_controller', __name__, url_prefix='/users')

# Initialize the movie service with the SQLite database file
DB_NAME = os.getenv('DB_NAME', 'moviwebapp.db')
if not DB_NAME:
    raise Exception("Movie DB Key not found in environment variables.")
movie_service = MovieService(DB_NAME)


@users_movie_controller.route('/', methods=['GET'])
def list_users():
    """
        Route to display the list of all users.
    """
    users = movie_service.get_all_users()
    logging.info("Rendered the users list page.")
    return render_template('users.html', users=users)

@users_movie_controller.route('/<int:user_id>', methods=['GET'])
def user_movies(user_id):
    """
    Route to display the movies of a specific user by user ID.
    """
    if not movie_service.get_user(user_id):
        raise NotFoundErr(f"User not found with ID:{user_id}")
    movies = movie_service.get_user_movies(user_id)
    user = next((u for u in movie_service.get_all_users() if u["id"] == user_id), None)

    message = request.args.get('message', '')
    status = request.args.get('status', '')

    logging.info(f"Rendered movies for user ID {user_id}.")
    return render_template("user_movies.html", movies=movies, user=user, message=message, status=status)

# Route: Add User
@users_movie_controller.route('/add', methods=['GET', 'POST'])
def add_user():
    """
       Route to add a new user.
    """
    if request.method == 'POST':
        try:
            name = UserValidator.validate_add_user()
            movie_service.add_user(name)
            logging.info(f"Added new user: {name}.")
            return redirect('/users')
        except BadRequest as e:
            logging.error(f"Error adding user: {str(e)}")
            return render_template('add_user.html', error_message=str(e))
    return render_template('add_user.html')


# Route: Add Movie
@users_movie_controller.route('/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """
       Route to add a new movie for a user.
    """
    if not movie_service.get_user(user_id):
        raise NotFoundErr(f"User not found with ID:{user_id}")
    if request.method == 'POST':
        try:
            name = MovieValidator.validate_add_movie()
            movie_service.add_movie(name, user_id)
            logging.info(f"Added movie '{name}' for user ID {user_id}.")
            return redirect(f'/users/{user_id}?message=Movie "{name}" added successfully!&status=success')
        except BadRequest as e:
            logging.error(f"Error adding movie for user ID {user_id}: {str(e)}")
            return redirect(f'/users/{user_id}?message={str(e)}&status=error')
    return render_template('add_movie.html', user_id=user_id)

@users_movie_controller.route('/<int:user_id>/update/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """
       Route to update an existing movie for a user.
    """
    if not movie_service.get_user(user_id) or not movie_service.get_movie(movie_id):
        raise NotFoundErr(f"User or movie not found with userId:{user_id}, movieid: {movie_id}")
    movies = movie_service.get_user_movies(user_id)
    movie = next((m for m in movies if m['id'] == movie_id), None)

    if not movie:
        raise NotFoundErr(f"Error updating movie for user ID {user_id}, movie ID {movie_id}")

    if request.method == 'POST':
        try:
            name, year, rating = MovieValidator.validate_update_movie()
            movie_service.update_movie(movie_id, name, year, rating)
            logging.info(f"Updated movie ID {movie_id} for user ID {user_id}.")


            return redirect(url_for('users_movie_controller.user_movies',
                                    user_id=user_id,
                                    message=f"Movie '{name}' updated successfully!",
                                    status='success'))
        except Exception as e:
            logging.error(f"Error updating movie for user ID {user_id}, movie ID {movie_id}: {str(e)}")
            return redirect(url_for('users_movie_controller.user_movies',
                                user_id=user_id,
                                message=f"Error updating movie with movie Id {movie_id}.",
                                status='error'))

    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie=movie)

@users_movie_controller.route('/<int:user_id>/delete/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """
        Route to delete a movie for a specific user.
    """
    if not movie_service.get_user(user_id) or not movie_service.get_movie(movie_id):
        raise NotFoundErr(f"User or movie not found with userId:{user_id}, movieid: {movie_id}")
    try:
        movie_service.delete_movie(movie_id)
        logging.info(f"Deleted movie ID {movie_id} for user ID {user_id}.")
        return redirect(url_for('users_movie_controller.user_movies',
                                user_id=user_id,
                                message=f"Movie with ID {movie_id} deleted successfully!",
                                status='success'))
    except Exception as e:
        logging.error(f"Error deleting movie ID {movie_id} for user ID {user_id}: {str(e)}")
        return redirect(url_for('users_movie_controller.user_movies',
                                user_id=user_id,
                                message=f"Error deleting movie with ID {movie_id}.",
                                status='error'))
