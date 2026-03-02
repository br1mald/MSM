from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import Optional


class WorkerSearchForm(FlaskForm):
    competence = StringField("Compétence", validators=[Optional()])

    dispo = SelectField(
        "Disponibilité",
        choices=[
            ("", "Toute disponibilité"),
            ("FLEXIBLE", "Flexible"),
            # ("Temps plein", "Temps plein"),
            ("MORNINGS", "Matin"),
            ("AFTERNOONS", "Après-midi"),
            ("EVENINGS", "Soir"),
            ("WEEKENDS", "Week-end"),
        ],
        validators=[Optional()],
    )

    note_min = SelectField(
        "Note minimum",
        choices=[
            ("0", "Toutes les notes"),
            ("3", "3★ et plus"),
            ("4", "4★ et plus"),
            ("5", "5★ uniquement"),
        ],
        validators=[Optional()],
    )

    submit = SubmitField("Filtrer")
