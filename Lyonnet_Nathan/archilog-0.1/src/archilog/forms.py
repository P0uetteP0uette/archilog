from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, FileField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class AddEntryForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    amount = DecimalField('Montant', validators=[DataRequired()])
    category = StringField('Catégorie', validators=[DataRequired()])


class EditEntryForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    amount = DecimalField('Montant', validators=[DataRequired()])
    category = StringField('Catégorie', validators=[DataRequired()])


class ImportCSVForm(FlaskForm):
    file = FileField("Importer un fichier CSV", validators=[DataRequired()])
    submit = SubmitField("Importer")