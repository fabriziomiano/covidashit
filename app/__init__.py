"""
Flask application factory
"""
import logging
import os

import click
from celery import Celery
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_from_directory
from flask_babel import Babel
from flask_compress import Compress
from flask_pymongo import PyMongo
from flask_sitemap import Sitemap

from config import config as app_config
from settings import LANGUAGES, TRANSLATION_DIRNAME

load_dotenv()
mongo = PyMongo()
babel = Babel()
sitemap = Sitemap()
compress = Compress()
celery = Celery(__name__)


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
            "favicon.ico", mimetype="image/vnd.microsoft.icon")


def get_environment():
    """Return app environment"""
    return os.environ.get('APPLICATION_ENV') or 'development'


def create_app():
    """Create the flask application"""
    env = get_environment()
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)
    app.config.from_object(app_config[env])
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = os.path.join(
        app.root_path, TRANSLATION_DIRNAME)
    compress.init_app(app)
    mongo.init_app(app)
    babel.init_app(app)
    sitemap.init_app(app)
    set_error_handlers(app)
    set_robots_txt_rule(app)
    set_favicon_rule(app)
    celery.config_from_object(app.config)
    celery.conf.update(app.config.get("CELERY_CONFIG", {}))

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

    from app.db_utils.create import CollectionCreator
    cc = CollectionCreator()

    creation_menu = {
        "national": cc.create_national_collection,
        "regional": cc.create_regional_collection,
        "provincial": cc.create_provincial_collections,
        "national-trends": cc.create_national_trends_collection,
        "regional-trends": cc.create_regional_trends_collection,
        "provincial-trends": cc.create_provincial_trends_collection,
        "regional-breakdown": cc.create_regional_breakdown_collection,
        "provincial-breakdown": cc.create_provincial_breakdown_collection,
        "national-series": cc.create_national_series_collection,
        "regional-series": cc.create_regional_series_collection,
        "provincial-series": cc.create_provincial_series_collection,
        "vax-admins": cc.create_vax_admins_collection,
        "vax-admins-summary": cc.create_vax_admins_summary_collection
    }

    @app.cli.command("create-collections")
    def populate_db():
        """Populate all the collections needed on mongoDB"""
        for _type in creation_menu:
            creation_menu[_type]()

    @app.cli.command("create")
    @click.argument("collection_type")
    def populate_collection(collection_type):
        """Populate a collection type on the DB"""
        allowed_types = [k for k in creation_menu]
        try:
            creation_menu[collection_type]()
        except KeyError:
            app.logger.error(
                f"Invalid collection type: {collection_type}. " +
                "Allowed types: [" + ", ".join(a for a in allowed_types) + "]"
            )

    return app
