import logging
from flask import render_template, redirect, url_for, Response, Blueprint
import archilog.models as models
import archilog.services as services
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, FileField, SubmitField
from wtforms.validators import DataRequired

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


auth = HTTPBasicAuth()

users = {
    "admin": {"name": "admin", "password": generate_password_hash("admin"), "roles": ["admin"]},
    "user": {"name": "user", "password": generate_password_hash("user"), "roles": ["user"]}
}

def check_admin():
    user = users.get(auth.current_user())
    return user and user["role"] == "admin"

@auth.verify_password
def verify_password(username, password) -> str:
    user = users.get(username)
    if user and check_password_hash(user["password"], password):
        return user  # Retourner le nom d'utilisateur au lieu de True/False

@auth.get_user_roles
def get_user_roles(user: dict) -> list[str]:
    return user["roles"]


web_ui = Blueprint("web", __name__)

@web_ui.route('/', methods=['GET'])
@auth.login_required # tous les users connectés peuvent accéder a cette route
def home():
    entries = models.get_all_entries()
    form = ImportCSVForm()
    return render_template('home.html', entries=entries, form=form, user=auth.current_user())



class AddEntryForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    amount = DecimalField('Montant', validators=[DataRequired()])
    category = StringField('Catégorie', validators=[DataRequired()])

@web_ui.route('/add', methods=['GET', 'POST'])
@auth.login_required(role="admin") # seul l'admin peut accéder à cette route
def add_entry():
    form = AddEntryForm()  # Créer une instance du formulaire
    if form.validate_on_submit():  # Valider le formulaire lorsqu'il est soumis
        # Si le formulaire est valide, récupérer les données et créer une nouvelle entrée
        name = form.name.data
        amount = form.amount.data
        category = form.category.data
        models.create_entry(name, amount, category)
        logging.warning(f"L'entrée {name}, {amount}, {category} a été ajouté")
        return redirect(url_for('web.home'))
    return render_template('add_entry.html', form=form)  # Passer le formulaire au template


# WTForms : on change le name amount category, -> comme des arguments de l'objet form
# ca va nous permettre d'aller dans nos html et changer les formulaires existants et pouvoir leur rajouter des conditions. faire des trucs dynamique quoi


class EditEntryForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    amount = DecimalField('Montant', validators=[DataRequired()])
    category = StringField('Catégorie', validators=[DataRequired()])

@web_ui.route('/edit/<int:id>', methods=['GET', 'POST'])
@auth.login_required(role="admin")  # seul l'admin peut accéder à cette route
def edit_entry(id):
    entry = models.get_entry(id)  # Récupérer l'entrée à partir de la base de données
    form = EditEntryForm(obj=entry)  # Créer le formulaire pré-rempli avec les données existantes
    if form.validate_on_submit():  # Valider le formulaire lorsqu'il est soumis
        # Si le formulaire est valide, récupérer les données et mettre à jour l'entrée
        name = form.name.data
        amount = form.amount.data
        category = form.category.data
        models.update_entry(id, name, amount, category)
        logging.warning(f"L'entrée {name}, {amount}, {category} a été modifié")
        return redirect(url_for('web.home'))
    return render_template('edit_entry.html', form=form, entry=entry)  # Passer le formulaire et l'entrée au template

@web_ui.route('/delete/<int:id>', methods=['GET'])
@auth.login_required(role="admin") # seul l'admin peut accéder à cette route
def delete_entry(id):
    models.delete_entry(id)
    logging.warning(f"L'entrée {id} a été supprimé")
    return redirect(url_for('web.home'))



class ImportCSVForm(FlaskForm):
    file = FileField("Importer un fichier CSV", validators=[DataRequired()])
    submit = SubmitField("Importer")

@web_ui.route('/import_csv', methods=['POST'])
@auth.login_required(role="admin")  # Seul l'admin peut accéder à cette route
def import_csv():
    form = ImportCSVForm()

    # Flask-WTF nécessite que le formulaire soit instancié avec les données du POST
    if form.validate_on_submit():
        csv_file = form.file.data  # Récupérer le fichier

        if not csv_file:
            logging.warning("Aucun fichier n'a été envoyé")
            return redirect(url_for('web.home'))

        try:
            services.import_from_csv(csv_file)  # Appel du service d'import
            logging.warning("Import CSV réussi")
        except Exception as e:
            logging.warning(f"Erreur lors de l'import CSV : {e}")

        return redirect(url_for('web.home'))

    # En cas de problème, on recharge la home avec les entrées et le formulaire
    entries = models.get_all_entries()
    return render_template('home.html', entries=entries, form=form)



@web_ui.route('/export_csv', methods=['GET'])
@auth.login_required # tous les users connectés peuvent accéder a cette route
def export_csv():
    output = services.export_to_csv()
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=entries.csv'}
    )