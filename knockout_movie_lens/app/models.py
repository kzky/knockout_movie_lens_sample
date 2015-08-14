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
        if limit is None:
            limit = 30
        else:
            limit = int(limit)
        users = [user for user in cls.users.find(limit=limit)]
        return cls.remove_id(users)

    @classmethod
    def get_user(cls, user_name):
        movie_names_ = cls.users.find_one({"user_name": user_name},
                                          {"movie_names": 1, "_id": 0})["movie_names"]
        movie_names = []
        for movie_name in movie_names_:
            movie_names.append(
                {"movie_name": movie_name}
            )
        return movie_names

class Movie(Base):
    movies = db[config.COL_MOVIES]

    def __init__(self, movie_name, movie_id):
        self.movie_name = movie_name
        self.movie_id = movie_id
    
    @classmethod
    def get_movies(cls, limit=30):
        if limit is None:
            limit = 30
        else:
            limit = int(limit)
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
    def get_c2c_results(cls, movie, limit=30):
        print limit
        c2c_result = cls.c2c_results.find_one({"movie": movie})
        if limit is None:
            limit = 30
        else:
            limit = int(limit)

        recommendations = c2c_result["recommendations"][0:limit]

        return recommendations
        
