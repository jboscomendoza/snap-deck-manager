from config import basedir
from flask import render_template, request, redirect, flash, url_for
from app.extensions import db
from app.decks import bp
from app.forms.decks import FormDecks
from app.models.decks import Deck

@bp.route("/", methods=["GET", "POST"])
def index():
    title="Deck manager"
    return render_template(
        "index.html",
        title=title,
        )

@bp.route("/add-decks/", methods=["GET", "POST"])
def add_decks():
    title="Add decks"
    form=FormDecks()
    if form.validate_on_submit() and request.method == "POST":
        deck = Deck(
            name = request.form["name"],
            decklist = request.form["decklist"],
        )
        db.session.add(deck)
        db.session.commit()
        flash("Deck added")
        return redirect(url_for(
            "decks.get_decks"
        ))
    return render_template(
        "add-decks.html",
        title=title,
        form=form,
    )

@bp.route("/get-decks/", methods=["GET", "POST"])
def get_decks():
    title="Get decks"
    decks = db.session.query(Deck)
    deck_items = []
    for i in decks:
        decklist = i.decklist.split("#")
        deck_cards = decklist[1:12]
        deck_dict = {
            "name"  : i.name,
            "cards" : "".join(deck_cards),
            "code"  : decklist[13],
        }
        deck_items.append(deck_dict)
    return render_template(
        "get-decks.html",
        title=title,
        deck_items=deck_items,
    )