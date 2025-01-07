import logging
from xml.dom import NotFoundErr

from sqlalchemy import func
from app.data_manager.sqlite_data_manager import SQLiteDataManager
from app.model.data_model import User, Movie
from app.services.omdb_api_service import OMDbAPIService


class MovieService:
    def __init__(self, db_file_name):
        """Initialize MovieService with a data manager and OMDb API service."""
        self.data_manager = SQLiteDataManager(db_file_name)
        self.omdb_api_service = OMDbAPIService()

    def get_all_users(self):
        """Fetch all users with their associated movie count."""
        session = self.data_manager.Session()
        try:
            # Query users with the count of movies they have added
            users_with_counts = (
                session.query(
                    User.id,
                    User.name,
                    func.count(Movie.id).label("movies_count")
                )
                .outerjoin(Movie, User.id == Movie.user_id)
                .group_by(User.id)
                .all()
            )

            return [
                {"id": user.id, "name": user.name, "movies_count": user.movies_count}
                for user in users_with_counts
            ]
        finally:
            session.close()

    def add_user(self, name):
        """Add a new user to the database."""
        return self.data_manager.add_user(name)

    def get_all_movies(self):
        """Fetch all movies from the database."""
        return self.data_manager

    def add_movie(self, name, user_id):
        """Add a movie to the database by fetching its details from OMDb API."""
        user = self.data_manager.get_user(user_id)
        if not user:
            raise NotFoundErr(f"user not found: {user_id}")

        # Fetch movie data using OMDb API
        movie_data = self.omdb_api_service.fetch_movie_data(name)
        if movie_data:
            name = movie_data['title']
            year = movie_data['year']
            rating = movie_data['rating']
        else:
            raise FileNotFoundError("Movie name not found")

        # Add the movie to the database
        self.data_manager.add_movie(name, year, rating, user_id)

    def update_movie(self, movie_id, new_name=None, new_year=None, new_rating=None):
        """
        Update movie details in the database, fetching updated data from OMDb API if necessary.
        If new_year or new_rating is None, it will take the values from the OMDb API or fallback to the existing database values.
        """
        existing_movie = self.data_manager.get_movie(movie_id)
        if not existing_movie:
            raise NotFoundErr(f"Movie with ID {movie_id} does not exist in the database.")

        movie_data = None
        if new_name:
            movie_data = self.omdb_api_service.fetch_movie_data(new_name)
            if movie_data:
                new_name = movie_data.get('title', new_name)
            else:
                raise NotFoundErr(f"Movie '{new_name}' not found in OMDb database.")

        new_year = new_year or (movie_data.get('year') if movie_data else existing_movie['year'])
        new_rating = new_rating or (movie_data.get('rating') if movie_data else existing_movie['rating'])

        self.data_manager.update_movie(movie_id, new_name, new_year, new_rating)
        logging.info(f"Movie with ID {movie_id} successfully updated.")

    def delete_movie(self, movie_id):
        """Delete a movie from the database."""
        self.data_manager.delete_movie(movie_id)

    def get_user(self, user_id):
        """Fetch a user by their ID."""
        return self.data_manager.get_user(user_id)

    def get_movie(self, movie_id):
        """Fetch a movie by its ID."""
        return self.data_manager.get_movie(movie_id)

    def get_user_movies(self, user_id):
        """Fetch all movies associated with a specific user, sorted by movie ID."""
        if not self.get_user(user_id):
            raise NotFoundErr(f"user not found: {user_id}")

        movies = self.data_manager.get_user_movies(user_id)
        return sorted(movies, key=lambda x: x['id'], reverse=True)
