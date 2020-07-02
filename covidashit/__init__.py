import atexit
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from flask_babel import Babel

from config import (
    LANGUAGES, TRANSLATION_DIRNAME, BCR_CRON_HOURS, BCR_CRON_MINUTES
)
from .datatools import barchartrace_html_to_mongo
from .views.dashboard import dashboard

mongo = PyMongo()
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=barchartrace_html_to_mongo,
    trigger="cron",
    hour=BCR_CRON_HOURS,
    minute=BCR_CRON_MINUTES
)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


def create_app():
    app = Flask("covidashit")
    app.config["MONGO_URI"] = os.environ["MONGO_URI"]
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

    set_error_handlers(app)
    app.register_blueprint(dashboard)
    return app


def set_error_handlers(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template("errors/500.html"), 500
