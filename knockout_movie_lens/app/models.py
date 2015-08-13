from app import db, app
import config

class User(object):
    def __init__(self, user_name, user_id):
        """
        """
        self.user_name = user_name
        self.user_id = user_id

class Movie(object):
    def __init__(self, movie_name, movie_id):

        self.movie_name = movie_name
        self.movie_id = movie_id
        
class C2CResult(object):
    def __init__(self, movie_name, score):
        self.movie_name = movie_name
        self.score = score
        pass

class BaseHelper(object):

    @classmethod
    def remove_id(cls, docs):
        if type(docs) == list:
            for doc in docs:
                del doc["_id"]
            pass
        if type(docs) == dict:
            del docs["_id"]

        return docs
        
class UsersHelper(BaseHelper):
    users = db[config.COL_USERS]

    @classmethod
    def get_users(cls, limit=30):
        users = [user for user in cls.users.find(limit=limit)]
        return cls.remove_id(users)

    @classmethod
    def get_user(cls, user_name):
        user = cls.users.find_one({"user_name": user_name})
        return cls.remove_id(user)

class MoviesHelper(BaseHelper):
    movies = db[config.COL_MOVIES]
    
    @classmethod
    def get_movies(cls, limit=30):
        movies = [movie for movie in cls.movies.find(limit=limit)]
        return cls.remove_id(movies)

    @classmethod
    def get_movie(cls, movie_name):
        movie = cls.movies.find_one({"movie_name": movie_name})
        return cls.remove_id(movie)

class C2CResultsHelper(BaseHelper):
    c2c_results = db[config.COL_C2C_RESULTS]
    
    @classmethod
    def get_c2c_results(cls, movie):
        c2c_result = cls.c2c_results.find_one({"movie": movie})
        recommendations = c2c_result["recommendations"]
        return recommendations

        
