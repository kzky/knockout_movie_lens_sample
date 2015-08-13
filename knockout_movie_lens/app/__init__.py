from flask import Flask, render_template
from pymongo import MongoClient
import config

# App
app = Flask(config.APP_NAME)

# Config
app.config.from_object('config')

# DB
client = MongoClient(app.config["DB_HOST"], app.config["DB_PORT"])
db = client.get_database(app.config["DB_NAME"])

# Error Handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.controllers import movie_lens as movie_lens

# Register blueprint(s)
app.register_blueprint(movie_lens)


