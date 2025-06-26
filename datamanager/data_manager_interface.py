from abc import ABC, abstractmethod

class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self): pass

    @abstractmethod
    def get_user(self, user_id): pass

    @abstractmethod
    def get_user_movies(self, user_id): pass

    @abstractmethod
    def add_user(self, name): pass

    @abstractmethod
    def add_movie(self, user_id, movie_data): pass

    @abstractmethod
    def update_movie(self, movie_id, updated_data): pass

    @abstractmethod
    def delete_movie(self, movie_id): pass
