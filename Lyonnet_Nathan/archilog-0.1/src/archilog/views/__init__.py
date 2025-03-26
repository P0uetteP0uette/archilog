import logging
from flask import Flask
from archilog.views.error_handler import register_error_handlers
from archilog.views.routes import web_ui

# Application factory
def create_app():

    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("archilog.log"),
            logging.StreamHandler()
        ]
    )

    app = Flask(__name__)
    app.config.from_prefixed_env(prefix="ARCHILOG_FLASK")
    
    register_error_handlers(app)

    app.register_blueprint(web_ui)

    return app