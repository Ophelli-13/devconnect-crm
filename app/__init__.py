from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt
from app.models import Lead,Message,User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
 

    @app.route('/health')
    def health_check():
        return {"status": "online", "project": "DevConnect CRM"}, 200

    return app