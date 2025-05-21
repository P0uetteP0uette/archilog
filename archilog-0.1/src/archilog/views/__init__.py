import logging

from flask import Flask

from archilog.views.api import api_views, register_spec  # Importer le Blueprint API
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
    
    # Enregistrer les Blueprints
    register_error_handlers(app)
    app.register_blueprint(web_ui)  # Blueprint pour les routes web
    app.register_blueprint(api_views)  # Blueprint pour l'API avec préfixe '/api'

    # Enregistrement de la documentation OpenAPI (Spectree)
    register_spec(app)

    return app