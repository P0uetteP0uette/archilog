import logging
from flask import render_template, redirect, url_for

def register_error_handlers(app):
    """enregistre les gestionnaires d'erreurs pour l'app flask"""

    # Erreur 404 (page non trouvée)
    @app.errorhandler(404)
    def page_not_found(error):
        """Gérer les erreurs 404 et logguer l'événemenrt"""
        logging.warning(f"404 - page not found : {error}")
        return render_template("404.html"), 404 #retourne page perso
    
    # Erreur 500 (erreur interne du serveur)
    @app.errorhandler(500)
    def handle_internal_error(error):
        """gerer les erruers 500 et logguer l'évé"""

        logging.critical(f"Erreur interne du servezur : {error}",exc_info=True)
        return redirect(url_for("home.html")) # redirection page d'accueil