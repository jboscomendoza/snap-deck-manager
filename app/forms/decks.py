from flask_wtf import FlaskForm
from wtforms import (
    StringField, SelectField, SubmitField, TextAreaField
)
from wtforms.validators import DataRequired, Length

class FormDecks(FlaskForm):
    name = StringField(
        "Deck name",
        validators=[
            DataRequired(),
            Length(max=32)
            ]
        )
    decklist = TextAreaField(
        "Deck list",
        validators=[
            DataRequired(),
            ],
        )
    tag = StringField(
        "Tag",
        validators=[
            DataRequired(),
            Length(max=32),
        ]
    )
    send = SubmitField("Send")
    