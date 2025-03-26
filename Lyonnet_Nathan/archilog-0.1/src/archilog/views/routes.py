import logging
from flask import render_template, request, redirect, url_for, Response, Blueprint
import archilog.models as models
import archilog.services as services
from archilog.forms import EditEntryForm, AddEntryForm

web_ui = Blueprint("web", __name__)


@web_ui.route('/')
def home():
    entries = models.get_all_entries()
    return render_template('home.html', entries=entries)

@web_ui.route('/add', methods=['GET', 'POST'])
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

@web_ui.route('/edit/<int:id>', methods=['GET', 'POST'])
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
def delete_entry(id):
    models.delete_entry(id)
    logging.warning(f"L'entrée {id} a été supprimé")
    return redirect(url_for('web.home'))

@web_ui.route('/import_csv', methods=['POST'])
def import_csv():
    csv_file = request.files['file']
    services.import_from_csv(csv_file)
    return redirect(url_for('web.home'))

@web_ui.route('/export_csv', methods=['GET'])
def export_csv():
    output = services.export_to_csv()
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=entries.csv'}
    )
