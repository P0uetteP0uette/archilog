import logging
from flask import Blueprint, jsonify, request
from flask_httpauth import HTTPTokenAuth
from archilog import models
from archilog.services import import_from_csv, export_to_csv
from spectree import SpecTree
from pydantic import BaseModel, ValidationError, Field

# Initialisation de l'authentification par token
auth = HTTPTokenAuth(scheme='Bearer')

# Exemple de base de données pour l'API
users_db = [{"name": "john", "age": "42"}, {"name": "jane", "age": "34"}]

# Définition du Blueprint pour l'API
api_bp = Blueprint('api', __name__)

# Définir le modèle de données utilisateur avec Pydantic
class UserData(BaseModel):
    name: str = Field(min_length=2, max_length=40)
    age: int = Field(gt=0, lt=150)

# Exemple d'authentification par token
@auth.verify_token
def verify_token(token):
    # Tu peux remplacer cette logique par un mécanisme réel d'authentification
    if token == "valid_token":
        return "user"
    return None

# Route GET pour lister les utilisateurs
@api_bp.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    return jsonify(users_db)

# Route POST pour ajouter un utilisateur
@api_bp.route('/users', methods=['POST'])
@auth.login_required
def add_user():
    try:
        # Valider et récupérer les données du corps de la requête
        user = UserModel(**request.json)
        users_db.append(user.dict())
        return jsonify(user.dict()), 201
    except ValidationError as e:
        return jsonify(e.errors()), 400

# Route PUT pour modifier un utilisateur
@api_bp.route('/users/<string:name>', methods=['PUT'])
@auth.login_required
def update_user(name):
    user = next((u for u in users_db if u['name'] == name), None)
    if user:
        data = UserModel(**request.json)
        user.update(data.dict())
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

# Route DELETE pour supprimer un utilisateur
@api_bp.route('/users/<string:name>', methods=['DELETE'])
@auth.login_required
def delete_user(name):
    global users_db
    users_db = [u for u in users_db if u['name'] != name]
    return '', 204

# Route GET pour exporter les entrées en CSV
@api_bp.route('/export_csv', methods=['GET'])
@auth.login_required
def export_csv():
    output = export_to_csv()
    return jsonify({
        "message": "Export CSV réussi",
        "data": output
    })

# Route POST pour importer des données CSV
@api_bp.route('/import_csv', methods=['POST'])
@auth.login_required
def import_csv():
    try:
        # Récupérer le fichier CSV de la requête
        csv_file = request.files['file']
        import_from_csv(csv_file)  # Appeler la fonction d'import
        return jsonify({"message": "Import CSV réussi"})
    except Exception as e:
        logging.error(f"Erreur lors de l'import CSV : {e}")
        return jsonify({"error": "Erreur lors de l'import CSV"}), 400

# Swagger et Spectree pour l'API
spec = SpecTree("flask")
spec.register(api_bp)

