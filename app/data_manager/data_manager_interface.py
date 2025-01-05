from abc import abstractmethod, ABC
from typing import List, Dict

class DataManagerInterface(ABC):

    @abstractmethod
    def add_user(self, name: str) -> int:
        pass

    @abstractmethod
    def add_movie(self, name: str, year: int, rating: float, user_id: int) -> bool:
        pass

    @abstractmethod
    def update_movie(self, movie_id: int, name: str = None, year: int = None, rating: float = None) -> bool:
        pass

    @abstractmethod
    def delete_movie(self, movie_id: int) -> bool:
        pass

    @abstractmethod
    def get_all_users(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def get_user_movies(self, user_id: int) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def get_user_favorites(self) -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def get_user(self, user_id: int) -> Dict[str, str]:
        pass

    @abstractmethod
    def get_movie(self, movie_id: int) -> Dict[str, str]:
        pass
