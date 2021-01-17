"""
Flask application factory
"""
import os

import click
from dotenv import load_dotenv
from flask import Flask, request, render_template, send_from_directory
from flask_babel import Babel
from flask_compress import Compress
from flask_pymongo import PyMongo
from flask_sitemap import Sitemap

from config import LANGUAGES, TRANSLATION_DIRNAME

load_dotenv()
mongo = PyMongo()
babel = Babel()
sitemap = Sitemap()
compress = Compress()


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


def create_app():
    """Create the flask application"""
    app = Flask(__name__)
    translation_dir = os.path.join(app.root_path, TRANSLATION_DIRNAME)
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = translation_dir
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["MONGO_URI"] = os.environ["MONGO_URI"]
    app.config["SITEMAP_INCLUDE_RULES_WITHOUT_PARAMS"] = True
    compress.init_app(app)
    mongo.init_app(app)
    babel.init_app(app)
    sitemap.init_app(app)
    set_error_handlers(app)
    set_robots_txt_rule(app)
    set_favicon_rule(app)

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

    from app.db.create import (
        create_national_collection, create_national_series_collection,
        create_national_trends_collection, create_regional_collection,
        create_regional_breakdown_collection,
        create_regional_series_collection,
        create_regional_trends_collection, create_provincial_collections,
        create_provincial_breakdown_collection,
        create_provincial_series_collection,
        create_provincial_trends_collection, create_vax_collection,
        create_vax_summary_collection
    )

    collection_creation = {
        "national": create_national_collection,
        "regional": create_regional_collection,
        "provincial": create_provincial_collections,
        "national_trends": create_national_trends_collection,
        "regional_trends": create_regional_trends_collection,
        "provincial_trends": create_provincial_trends_collection,
        "regional_breakdown": create_regional_breakdown_collection,
        "provincial_breakdown": create_provincial_breakdown_collection,
        "national_series": create_national_series_collection,
        "regional_series": create_regional_series_collection,
        "provincial_series": create_provincial_series_collection,
        "vax": create_vax_collection,
        "vax_summary": create_vax_summary_collection
    }

    @app.cli.command("create-collections")
    def populate_db():
        """Populate all the collections needed on mongoDB"""
        for coll_type in collection_creation:
            collection_creation[coll_type]()

    @app.cli.command("create")
    @click.argument("collection_type")
    def populate_collection(collection_type):
        """
        Populate a collection_type ob mongoDB.
        Choose one of the following:
        "national", "regional", "provincial", "latest_regional",
        "latest_provincial", "national_trends", "regional_trends",
        "provincial_trends", "regional_breakdown", "provincial_breakdown",
        "national_series", "regional_series", "provincial_series",
        "vax", "vax_summary"
        """
        collection_creation[collection_type]()

    return app
