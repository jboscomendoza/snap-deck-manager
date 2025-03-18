from config import basedir
from flask import render_template, request
from app.extensions import db
from app.decks import bp
from app.forms.decks import FormDecks
from app.models.decks import Deck

@bp.route("/", methods=["GET", "POST"])
def index():
    title="Index"
    return render_template(
        "index.html",
        title=title,
        )