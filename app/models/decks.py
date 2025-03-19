from app.extensions import db

deck_tag = db.Table(
    "deck_tag",
    db.Column("deck_id", db.Integer, db.ForeignKey("decks.id")),
    db.Column("tag_id",  db.Integer, db.ForeignKey("tags.id")),
    )

class Deck(db.Model):
    __tablename__ = "decks"
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(32), nullable=False)
    decklist = db.Column(db.Text, nullable=False)
    tags = db.relationship("Tag", secondary=deck_tag, backref="decks")
    def __repr__(self):
        return f"<Deck: '{self.name}'>"

class Tag(db.Model):
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    def __repr__(self):
        return f"<Tag: '{self.name}'>"