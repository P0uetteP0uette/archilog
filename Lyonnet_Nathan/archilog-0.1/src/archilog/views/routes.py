from flask import render_template, request, redirect, url_for, Response, flash
import archilog.models as models
import archilog.services as services
from archilog.web_ui import web_ui

@web_ui.route('/')
def home():
    entries = models.get_all_entries()
    return render_template('home.html', entries=entries)

@web_ui.route('/add', methods=['GET', 'POST'])
def add_entry():
    if request.method == 'POST':
        try:
            name = request.form['name']
            amount = float(request.form['amount'])
            category = request.form['category']
            models.create_entry(name, amount, category)
            flash("Entrée ajoutée avec succès", "success")
            return redirect(url_for('web.home'))
        except ValueError:
            flash("Erreur: Montant invalide", "error")
            return render_template('add_entry.html')
    return render_template('add_entry.html')

@web_ui.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_entry(id):
    try:
        entry = models.get_entry(id)
        if request.method == 'POST':
            name = request.form['name']
            amount = float(request.form['amount'])
            category = request.form['category']
            models.update_entry(id, name, amount, category)
            flash("Entrée modifiée avec succès", "success")
            return redirect(url_for('web.home'))
        return render_template('edit_entry.html', entry=entry)
    except Exception as e:
        flash(f"Erreur: {str(e)}", "error")
        return redirect(url_for('web.home'))

@web_ui.route('/delete/<int:id>', methods=['GET'])
def delete_entry(id):
    try:
        models.delete_entry(id)
        flash("Entrée supprimée avec succès", "success")
    except Exception as e:
        flash(f"Erreur: {str(e)}", "error")
    return redirect(url_for('web.home'))

@web_ui.route('/import_csv', methods=['POST'])
def import_csv():
    try:
        csv_file = request.files['file']
        services.import_from_csv(csv_file)
        flash("Importation CSV réussie", "success")
    except Exception as e:
        flash(f"Erreur lors de l'importation: {str(e)}", "error")
    return redirect(url_for('web.home'))

@web_ui.route('/export_csv', methods=['GET'])
def export_csv():
    try:
        output = services.export_to_csv()
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=entries.csv'}
        )
    except Exception as e:
        flash(f"Erreur lors de l'exportation: {str(e)}", "error")
        return redirect(url_for('web.home'))