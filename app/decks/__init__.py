from flask import Blueprint
from app.forms import decks

bp = Blueprint("decks", __name__)

from app.decks import routes