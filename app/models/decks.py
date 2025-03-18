from app.extensions import db

class Deck(db.Model):
    __tablename__ = "decks"
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(32), nullable=False)
    decklist = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return f"<Deck: '{self.name}'>"