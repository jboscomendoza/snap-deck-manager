from flask_wtf import FlaskForm
from wtforms import (
    StringField, RadioField, SubmitField, TextAreaField
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
        "Tags",
        description="Multiple tags separated by commas.",
        validators=[
            DataRequired(),
            Length(max=32),
        ]
    )
    send = SubmitField("Send")

class DeleteDeck(FlaskForm):
    confirm = RadioField(
        "Confirm deletion", 
        choices=["No", "Yes"],
        default="No"
        )
    send = SubmitField("Send")