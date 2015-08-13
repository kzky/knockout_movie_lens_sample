from flask import Blueprint, render_template, make_response
from flask.json import jsonify
import json

from app import app
from app.models import UsersHelper, MoviesHelper, C2CResultsHelper

movie_lens = Blueprint('movie_lens', __name__, url_prefix='/movie_lens')

@movie_lens.route("/test")
def test():

    data = {"test": "test!"}
    app.logger.debug(data)
    return jsonify(data)

@movie_lens.route("/users")
def users():
    users_ = UsersHelper.get_users()
    users = json.dumps(users_)
    return make_response(users)

@movie_lens.route("/users/<int:user>")
def user(user):
    user = UsersHelper.get_user(user)
    app.logger.debug(user)
    return jsonify(user)

@movie_lens.route("/movies")
def movies():
    movies_ = MoviesHelper.get_movies()
    movies = json.dumps(movies_)
    return make_response(movies)

@movie_lens.route("/movies/<int:movie>")
def movie(movie):
    movie = MoviesHelper.get_movie(movie)

    return jsonify(movie)

@movie_lens.route("/c2c_results/<int:movie>")
def c2c_results(movie):
    movies_ = C2CResultsHelper.get_c2c_results(movie)
    movies = json.dumps(movies_)
    return make_response(movies)


    
