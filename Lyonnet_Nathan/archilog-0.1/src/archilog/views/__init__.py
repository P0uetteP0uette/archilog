from flask import Blueprint

web_ui = Blueprint("web", __name__, template_folder="templates")

from archilog.views.routes import *  # Importer toutes les routes