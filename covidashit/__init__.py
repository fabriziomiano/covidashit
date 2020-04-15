import os

from flask import Flask, request, render_template
from flask_babel import Babel

from config import LANGUAGES, WEBSITE_TITLE
from .views.dashboard import dashboard


def create_app():
    app = Flask(__name__)
    babel = Babel(app)
    set_error_handlers(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(LANGUAGES.keys())

    app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(
        app.root_path, "translations")

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

    set_error_handlers(app)
    app.register_blueprint(dashboard)
    return app


def set_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html", pagetitle=WEBSITE_TITLE), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("500.html", pagetitle=WEBSITE_TITLE), 500
