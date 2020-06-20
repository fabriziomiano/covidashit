import atexit
import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request, render_template
from flask_babel import Babel

from config import (
    LANGUAGES, TRANSLATION_DIRNAME, BARCHART_CRON_DT,
    BARCHART_CRON_LOG_FILENAME
)
from .datatools import barchartrace_to_html
from .views.dashboard import dashboard

scheduler = BackgroundScheduler()
scheduler.add_job(
    func=barchartrace_to_html,
    trigger="cron",
    hour=BARCHART_CRON_DT.hour,
    minute=BARCHART_CRON_DT.minute
)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def create_app():
    app = Flask("covidashit")
    babel = Babel(app)
    set_error_handlers(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(LANGUAGES.keys())

    app.config["BARCHART_LOG_PATH"] = os.path.join(
        app.root_path, BARCHART_CRON_LOG_FILENAME
    )
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
