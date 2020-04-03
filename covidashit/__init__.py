import os
from flask import Flask, request
from flask_babel import Babel
from config import LANGUAGES


app = Flask(__name__)
babel = Babel(app)
app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(
    app.root_path, "translations")


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

from covidashit import routes, views
