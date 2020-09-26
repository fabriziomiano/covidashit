import os

from flask import Flask, request, render_template
from flask_babel import Babel
from flask_pymongo import PyMongo

from config import (
    LANGUAGES, TRANSLATION_DIRNAME, MONGO_URI
)

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = MONGO_URI
    mongo.init_app(app)
    babel = Babel(app)
    set_error_handlers(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(LANGUAGES.keys())

    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(
        app.root_path, TRANSLATION_DIRNAME
    )

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

    from .ui import dashboard
    app.register_blueprint(dashboard)

    from .api import api
    app.register_blueprint(api)

    return app


def set_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.error("{}".format(e))
        return render_template("errors/404.html", error=e), 404

    @app.errorhandler(400)
    @app.errorhandler(405)
    @app.errorhandler(500)
    def server_error(e):
        app.logger.error("{}".format(e))
        return render_template("errors/generic.html", error=e)
