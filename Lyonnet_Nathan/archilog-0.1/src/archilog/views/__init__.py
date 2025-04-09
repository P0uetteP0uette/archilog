import logging
from flask import Flask
from archilog.views.error_handler import register_error_handlers
from archilog.views.routes import web_ui
from archilog.views.api import api_bp  # Importer le Blueprint API
from spectree import SpecTree, SecurityScheme

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
    app.register_blueprint(api_bp)  # Blueprint pour l'API avec préfixe '/api'

    # Swagger et Spectree pour l'API
    spec = SpecTree(
        "flask",
        security_schemes=[SecurityScheme(
            name="bearer_token",
            data={"type": "http", "scheme": "bearer"}
        )],
        security=[{"bearer_token": []}]
    )
    spec.register(app)  # Enregistrer Swagger

    return app