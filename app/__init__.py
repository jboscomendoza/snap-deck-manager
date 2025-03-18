from flask import Flask
from flask_bootstrap import Bootstrap5

from config import Config
from app.extensions import(
    db, migrate, metadata
)

from app import models

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Extensions
    ## db
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    
    ## Bootstrap
    app.config["BOOTSTRAP_BOOTSWATCH_THEME"] = "lux"
    bootstrap = Bootstrap5(app)
    
    # Blueprints
    from app.decks import bp as bp_decks
    app.register_blueprint(bp_decks)
    
    return app