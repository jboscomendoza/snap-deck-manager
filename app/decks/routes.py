from config import basedir
from flask import (
    render_template, request, redirect, flash, url_for, abort
    )
from app.extensions import db
from app.decks import bp
from app.forms.decks import FormDecks
from app.models.decks import Deck, Tag
import re
import json
from os import path


PATH_CARDS_JSON = path.join(
    "app",
    "marvel-snap-cards",
    "marvel-snap-cards.json"
    )
UNIQUE_ENERGY = [str(i) for i in range(9)]

with open(PATH_CARDS_JSON, mode="r") as f:
    cards = json.load(f)

@bp.route("/", methods=["GET", "POST"])
def index():
    title="Home"
    urls = {
        "Add decks":"add_decks",
        "Get decks":"get_decks",
        "Get tags" :"get_tags",
        }
    return render_template(
        "index.html",
        title=title,
        urls=urls,
        )

@bp.route("/add-decks/", methods=["GET", "POST"])
def add_decks():
    title="Add new deck"
    form=FormDecks()
    if form.validate_on_submit() and request.method == "POST":
        deck_name     = request.form["name"]
        deck_decklist = request.form["decklist"]
        tag_names     = request.form["tag"]
        tag_names = tag_names.split(",")
        deck_tags = [Tag(name=i.strip()) for i in tag_names]
        deck = Deck(
            name     = deck_name,
            decklist = deck_decklist,
        )
        [deck.tags.append(i) for i in deck_tags]
        db.session.add(deck)
        db.session.commit()
        flash("Deck added.")
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
    title="Decks"
    decks = db.session.query(Deck)
    deck_items = []
    for i in decks:
        decklist = i.decklist.split("#")
        deck_cards = decklist[1:12]
        deck_dict = {
            "name"  : i.name,
            "cards" : "".join(deck_cards),
            "code"  : decklist[13],
            "tag"   : i.tags,
        }
        deck_items.append(deck_dict)
    return render_template(
        "get-decks.html",
        title=title,
        deck_items=deck_items,
        decks=decks,
    )

@bp.route("/tag/", methods=["GET"])
@bp.route("/tag/<string:tag>/", methods=["GET"])
def get_tags(tag=None):
    if not tag:
        title = "Tags"
        tags = db.session.execute(
            db.select(Tag)
        ).scalars()
        return render_template(
            "get-tags.html",
            tags=tags,
            title=title,
        )
    else:
        title = f"Decks with tag: {tag}"
        decks = db.session.execute(
            db.select(Deck).join(Deck.tags).filter(Tag.name == tag)
        ).scalars()
        return render_template(
            "get-decks.html",
            title=title,
            decks=decks,
            )

@bp.route("/deck/<int:id>/", methods=["GET", "POST"])
def view_deck(id):
    deck = db.first_or_404(
        db.select(Deck).filter_by(id=id)
    )
    raw_decklist = deck.decklist
    raw_decklist = raw_decklist.split("#")
    # 1:12 is the position of the card names in a standard decklist
    decklist = [re.sub(r"\(.\) ", "", i) for i in raw_decklist[1:12]]
    raw_energy = [re.findall(r"\((\d)\)", i)[0] for i in raw_decklist[1:12]]
    unique_energy = UNIQUE_ENERGY
    count_energy = [raw_energy.count(i) for  i in unique_energy]
    energy=dict(zip(unique_energy, count_energy))

    decklist = [i.strip() for i in decklist]
    # 23 is the position of the deck code in a standard decklist
    deck_code = raw_decklist[13]
    return render_template(
        "deck.html",
        title="Deck: " + deck.name,
        deck=deck,
        decklist=decklist,
        deck_code=deck_code,
        energy=energy,
    )

@bp.route("/card/<string:cardname>")
def view_card(cardname):
    title = cardname
    for i in cards:
        if i["name"] == cardname:
            card_data = i
            break
        else:
            card_data = None
    keys = ("energy", "power", "ability", "series")
    if not card_data:
        return abort(404)
    return render_template(
        "card.html",
        title=title,
        card_data=card_data,
        keys=keys,
    )

@bp.errorhandler(404)
def page_not_found(e):
    title="Page not found"
    return render_template(
        "404.html",
        title=title,
        )