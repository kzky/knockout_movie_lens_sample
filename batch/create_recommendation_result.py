#!/usr/bin/env python
from scipy.sparse import coo_matrix
import csv
from pymongo import MongoClient
import numpy as np

# mongo cilent
def init_db():
    """
    """
    client = MongoClient('localhost', 27017)
    db_name = 'movie_lens'
    client.drop_database(db_name)
    db = client.get_database(db_name)
    return db

def create_index(
        filepath):
        
    # indexing
    user_set = set()
    movie_set = set()
    
    with open(filepath) as fpin:
        reader = csv.reader(fpin, delimiter=",")
        for r in reader:
            user_set.add(int(r[0]))
            movie_set.add(int(r[1]))
            
    user_index = dict()
    for i, user in enumerate(user_set):
        user_index[user] = i
        pass
    
    movie_index = dict()
    for i, movie in enumerate(movie_set):
        movie_index[movie] = i
        pass

    return user_index, movie_index

def create_user_collection(db, user_index):
    users = db.users
    bulk = users.initialize_unordered_bulk_op()
    for name, index in user_index.items():
        bulk.insert(
            {
                "user_name": name,
                "user_id": index
            }
        )
        
    try:
        bulk.execute()
    except Exception:
        pass
    
def create_movie_collection(db, movie_index):
    movies = db.movies
    bulk = movies.initialize_unordered_bulk_op()
    for name, index in movie_index.items():
        bulk.insert(
            {
                "movie_name": name,
                "movie_id": index
            }
        )
        
    try:
        bulk.execute()
    except Exception:
        pass

def create_coo_matrix(filepath, user_index, movie_index):
    # coo mat
    row = []
    col = []
    data = []
    with open(filepath) as fpin:
        reader = csv.reader(fpin, delimiter=",")
        for r in reader:
            row.append(user_index[int(r[0])])
            col.append(movie_index[int(r[1])])
            data.append(float(r[2]))
    
        return coo_matrix((data, (row, col)))

def compute_c2c_results(coo_mat):
    return coo_mat.transpose().dot(coo_mat)

def create_c2c_collection(db, movie_index, c2c_results, upto=100):
    inv_movie_index = {v: k for k, v in movie_index.items()}
    c2c_results_col = db.c2c_results
    bulk = c2c_results_col.initialize_unordered_bulk_op()
    
    # very slow code
    for i in xrange(c2c_results.shape[0]):
        movie = inv_movie_index[i]
        results = c2c_results.getrow(i)

        # normalize in such a way of summing up all to 100
        total_score = np.sum(results.data)
        c2c_tuple = zip(results.indices,
                        list(100 * np.asarray(results.data) / total_score))

        # limit results
        c2c_limited = sorted(c2c_tuple, key=lambda x: x[1], reverse=True)[0:upto]

        # save c2c results
        recommendations = []
        for index, score in c2c_limited:
            recommendations.append(
                {"movie": inv_movie_index[index], "score": score}
            )
        data = {
            "movie": movie,
            "recommendations": recommendations
        }
        bulk.insert(data)
        if (i + 1) % 1000 == 0:
            try:
                print "bulk.execute at {}".format(i)
                bulk.execute()
                bulk = c2c_results_col.initialize_unordered_bulk_op()
            except Exception as e:
                print e
                pass
        
        pass
    try:
        print "bulk.execute at last."
        bulk.execute()
    except Exception as e:
        print e
        pass
    pass

def main():
    db = init_db()
    filepath = "./dataset/ratings_3cols.dat"

    user_index, movie_index = create_index(filepath)
    create_user_collection(db, user_index)
    create_movie_collection(db, movie_index)
    
    coo_mat = create_coo_matrix(filepath, user_index, movie_index)
    c2c_results = compute_c2c_results(coo_mat)

    create_c2c_collection(db, movie_index, c2c_results)

    pass

if __name__ == '__main__':
    main()
