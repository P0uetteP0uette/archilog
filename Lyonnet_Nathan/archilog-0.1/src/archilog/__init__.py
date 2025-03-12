from dataclasses import dataclass
import os
from flask import Flask
from flask import flash, redirect, url_for

@dataclass
class Config:
    DATABASE_URL: str
    DEBUG: bool

# Chargement de la configuration depuis les variables d'environnement
config = Config(
    DATABASE_URL=os.getenv("ARCHILOG_DATABASE_URL", "sqlite:///data.db"),
    DEBUG=os.getenv("ARCHILOG_DEBUG", "False") == "True"
)

# Application factory
def create_app():
    app = Flask(__name__)

    from archilog.views import web_ui
    app.config.from_prefixed_env(prefix="ARCHILOG_FLASK")
    from archilog.models import init_db
    init_db()
    app.register_blueprint(web_ui)
    
    # Gestion des erreurs
    @app.errorhandler(500)
    def handle_internal_error(error):
        flash("Erreur interne du serveur", "error")
        return redirect(url_for("web.home"))
    
    @app.errorhandler(404)
    def handle_not_found(error):
        flash("Page non trouvée", "error")
        return redirect(url_for("web.home"))
    
    return app