from flask import Flask, render_template

# app
app = Flask(__name__)

# config
app.config.from_object('config')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.controllers import root as root

# Register blueprint(s)
app.register_blueprint(root)


