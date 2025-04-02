import logging
from flask import render_template, request, redirect, url_for, Response, Blueprint
import archilog.models as models
import archilog.services as services
from archilog.forms import EditEntryForm, AddEntryForm, ImportCSVForm

web_ui = Blueprint("web", __name__)


@web_ui.route('/', methods=['GET', 'POST'])
def home():
    entries = models.get_all_entries()
    form = ImportCSVForm()
    return render_template('home.html', entries=entries, form=form)

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

@web_ui.route('/import_csv', methods=['GET', 'POST'])
def import_csv():
    form = ImportCSVForm()
    
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

    return render_template('home.html', form=form)

@web_ui.route('/export_csv', methods=['GET'])
def export_csv():
    output = services.export_to_csv()
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=entries.csv'}
    )
