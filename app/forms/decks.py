from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, SubmitField, TextAreaField
)
from wtforms.validators import DataRequired

class FormDecks(FlaskForm):
    name = StringField(
        "Deck name",
        validators=[
            DataRequired(),
            ]
        )
    decklist = TextAreaField(
        "Deck list",
        validators=[
            DataRequired(),
            ],
        )
    send = SubmitField("Send")
    