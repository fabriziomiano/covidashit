"""
Flask application factory
"""
import logging
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, send_from_directory
from flask_assets import Bundle, Environment
from flask_babel import Babel
from flask_compress import Compress
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_pymongo import PyMongo
from flask_sitemap import Sitemap

from config import config as app_config
from settings import LANGUAGES, TRANSLATION_DIRNAME

load_dotenv()
mongo = PyMongo()
babel = Babel(default_timezone="Europe/Rome")
sitemap = Sitemap()
compress = Compress()
limiter = Limiter(key_func=get_remote_address)
assets = Environment()


@babel.localeselector
def get_locale():
    """Return the locale that best match the client request"""
    return request.accept_languages.best_match(LANGUAGES.keys())


def set_error_handlers(app):
    """Error handler"""

    @app.errorhandler(404)
    def page_not_found(e):
        """Page not found"""
        app.logger.error("{}".format(e))
        return render_template("errors/404.html", error=e), 404

    @app.errorhandler(500)
    def server_error(e):
        """Generic server error"""
        app.logger.error("{}".format(e))
        return render_template("errors/generic.html", error=e)


def set_robots_txt_rule(app):
    """Bots rule"""

    @app.route("/robots.txt")
    def robots_txt():
        """Serve the robots.txt file"""
        return send_from_directory(app.static_folder, request.path[1:])


def set_favicon_rule(app):
    """Favicon rule"""

    @app.route("/favicon.ico")
    def favicon():
        """Serve the favicon.ico file"""
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )


def get_environment():
    """Return app environment"""
    return os.environ.get("APPLICATION_ENV") or "development"


def create_app():
    """Create the flask application"""
    env = get_environment()
    app = Flask("covidashit")
    app.logger.setLevel(logging.INFO)
    app.config.from_object(app_config[env])
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = os.path.join(
        app.root_path, TRANSLATION_DIRNAME
    )
    set_error_handlers(app)
    set_robots_txt_rule(app)
    set_favicon_rule(app)
    compress.init_app(app)
    mongo.init_app(app)
    babel.init_app(app)
    sitemap.init_app(app)
    limiter.init_app(app)
    bundles = {
        "common_css": Bundle(
            "css/styles.css", output="bundles/common.min.css", filters="cssmin"
        ),
        "pandemic_js": Bundle(
            "js/scripts.js",
            "js/pandemic-charts.js",
            output="bundles/pandemic.min.js",
            filters="jsmin",
        ),
        "vaccines_js": Bundle(
            "js/scripts.js",
            "js/vaccines-charts.js",
            output="bundles/vaccines.min.js",
            filters="jsmin",
        ),
    }

    assets.init_app(app)
    assets.register(bundles)

    @app.after_request
    def add_header(r):
        """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
        """
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        r.headers["Cache-Control"] = "public, max-age=0"
        return r

    from .ui import pandemic, vaccines

    app.register_blueprint(pandemic)
    app.register_blueprint(vaccines)

    from .api import api

    app.register_blueprint(api)

    return app
