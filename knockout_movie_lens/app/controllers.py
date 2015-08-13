from flask import Blueprint, render_template, make_response, request
from flask.json import jsonify
import json

from app import app
from app.models import User, Movie, C2CResults

movie_lens = Blueprint('movie_lens', __name__, url_prefix='/movie_lens')

@movie_lens.route("/test")
def test():

    data = {"test": "test!"}
    app.logger.debug(data)
    return jsonify(data)

@movie_lens.route("/users")
def users():
    limit = request.args.get("limit")
    users_ = User.get_users(limit)
    users = json.dumps(users_)
    return make_response(users)

@movie_lens.route("/users/<int:user>")
def user(user):
    user = User.get_user(user)
    app.logger.debug(user)
    return jsonify(user)

@movie_lens.route("/movies")
def movies():
    limit = request.args.get("limit")
    movies_ = Movie.get_movies(limit)
    movies = json.dumps(movies_)
    return make_response(movies)

@movie_lens.route("/movies/<int:movie>")
def movie(movie):
    movie = Movie.get_movie(movie)
    return jsonify(movie)

@movie_lens.route("/c2c_results/<int:movie>")
def c2c_results(movie):
    limit = request.args.get("limit")
    movies_ = C2CResults.get_c2c_results(movie, limit)
    movies = json.dumps(movies_)
    return make_response(movies)

