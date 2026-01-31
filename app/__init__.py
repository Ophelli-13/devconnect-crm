from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt

def create_app(config_cllas=Config):
    app = Flask(__name__)
    app.config.from_object(config_cllas)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route('/health')
    def health_check():
        return {"status": "online", "project": "DevConnect CRM"}, 200
    
    return app