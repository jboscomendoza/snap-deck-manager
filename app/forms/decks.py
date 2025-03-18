from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, SubmitField, TextAreaField
)
from wtforms.validators import DataRequired

class FormDecks(FlaskForm):
    deck_name = StringField(
        "Deck name",
        validators=[
            DataRequired(),
        ]
        )
    send = SubmitField("Send")
    