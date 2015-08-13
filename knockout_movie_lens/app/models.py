from app import db, app
import config

class Base(object):
    
    @classmethod
    def remove_id(cls, docs):
        if type(docs) == list:
            for doc in docs:
                del doc["_id"]
            
        if type(docs) == dict:
            del docs["_id"]

        return docs


class User(Base):
    users = db[config.COL_USERS]
    
    def __init__(self, user_name, user_id):
        self.user_name = user_name
        self.user_id = user_id

    @classmethod
    def get_users(cls, limit=30):
        users = [user for user in cls.users.find(limit=limit)]
        return cls.remove_id(users)

    @classmethod
    def get_user(cls, user_name):
        user = cls.users.find_one({"user_name": user_name})
        return cls.remove_id(user)

class Movie(Base):
    movies = db[config.COL_MOVIES]

    def __init__(self, movie_name, movie_id):
        self.movie_name = movie_name
        self.movie_id = movie_id
    
    @classmethod
    def get_movies(cls, limit=30):
        movies = [movie for movie in cls.movies.find(limit=limit)]
        return cls.remove_id(movies)

    @classmethod
    def get_movie(cls, movie_name):
        movie = cls.movies.find_one({"movie_name": movie_name})
        return cls.remove_id(movie)
        
class C2CResults(Base):
    c2c_results = db[config.COL_C2C_RESULTS]
    
    def __init__(self, movie_name, score):
        self.movie_name = movie_name
        self.score = score
    
    @classmethod
    def get_c2c_results(cls, movie):
        c2c_result = cls.c2c_results.find_one({"movie": movie})
        recommendations = c2c_result["recommendations"]
        return recommendations
        
