import logging
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.data_manager.data_manager_interface import DataManagerInterface  # Interface for data manager
from app.model.data_model import Base, User, Movie

logging.basicConfig(level=logging.ERROR)

class SQLiteDataManager(DataManagerInterface):
    def __init__(self, db_file_name):
        # Initialize the database connection and create tables if they don't exist
        db_path = 'data'
        if not os.path.exists(db_path):
            os.makedirs(db_path)
        self.engine = create_engine(f'sqlite:///{db_path}/{db_file_name}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_user(self, name):
        # Add a new user to the database
        session = self.Session()
        try:
            new_user = User(name=name)
            session.add(new_user)
            session.commit()
            return new_user.id
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding user: {e}")
            return None
        finally:
            session.close()

    def add_movie(self, name, year, rating, user_id):
        # Add a new movie for a user
        if not name or not isinstance(name, str):
            logging.error("Invalid movie name.")
            return False
        if not (0 <= rating <= 10):
            logging.error("Rating must be between 0 and 10.")
            return False
        session = self.Session()
        try:
            new_movie = Movie(name=name, year=year, rating=rating, user_id=user_id)
            session.add(new_movie)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Error adding movie:{e}")
        finally:
            session.close()

    def update_movie(self, movie_id, name=None, year=None, rating=None):
        # Update the details of an existing movie
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if not movie:
                logging.error(f"Movie with id {movie_id} not found.")
                return
            if name:
                movie.name = name
            if year:
                movie.year = year
            if rating:
                movie.rating = rating
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Error updating movie: {e}")
        finally:
            session.close()

    def delete_movie(self, movie_id):
        # Delete a movie from the database
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if not movie:
                logging.error(f"Movie with id {movie_id} not found.")
                return
            session.delete(movie)
            session.commit()
        except Exception as e:
            session.rollback()
            logging.error(f"Error deleting movie: {e}")
        finally:
            session.close()

    def get_user(self, user_id):
        # Retrieve user details by user ID
        session = self.Session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user:
                return {"id": user.id, "name": user.name}
            else:
                logging.error(f"User with ID {user_id} not found.")
                return None
        except Exception as e:
            logging.error(f"Error retrieving user with ID {user_id}: {e}")
            return None
        finally:
            session.close()

    def get_movie(self, movie_id):
        # Retrieve movie details by movie ID
        session = self.Session()
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                return {"id": movie.id, "name": movie.name}
            else:
                logging.error(f"User with ID {movie} not found.")
                return None
        except Exception as e:
            logging.error(f"Error retrieving movie with ID {movie_id}: {e}")
            return None
        finally:
            session.close()

    def get_all_users(self):
        # Retrieve all users from the database
        session = self.Session()
        try:
            users = session.query(User).all()
            return [{"id": user.id, "name": user.name} for user in users]
        except Exception as e:
            logging.error(f"Error retrieving users: {e}")
            return []
        finally:
            session.close()

    def get_user_movies(self, user_id):
        # Retrieve all movies associated with a specific user
        session = self.Session()
        try:
            movies = session.query(Movie).filter_by(user_id=user_id).all()
            return [
                {"id": movie.id, "name": movie.name, "year": movie.year, "rating": movie.rating}
                for movie in movies
            ]
        except Exception as e:
            logging.error(f"Error retrieving movies: {e}")
            return []
        finally:
            session.close()

    def get_user_favorites(self):
        # Retrieve each user's favorite movie (highest rated)
        session = self.Session()
        try:
            favorites = session.query(
                Movie.user_id,
                Movie.name,
                Movie.rating
            ).distinct(Movie.user_id).order_by(Movie.user_id, Movie.rating.desc()).all()
            return [
                {"user_id": user_id, "favorite_movie": name, "rating": rating}
                for user_id, name, rating in favorites
            ]
        except Exception as e:
            logging.error(f"Error retrieving user favorites: {e}")
            return []
        finally:
            session.close()
