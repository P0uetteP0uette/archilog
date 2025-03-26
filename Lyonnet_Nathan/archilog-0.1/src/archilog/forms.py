from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired


class AddEntryForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    amount = DecimalField('Montant', validators=[DataRequired()])
    category = StringField('Catégorie', validators=[DataRequired()])


class EditEntryForm(FlaskForm):
    name = StringField('Nom', validators=[DataRequired()])
    amount = DecimalField('Montant', validators=[DataRequired()])
    category = StringField('Catégorie', validators=[DataRequired()])
