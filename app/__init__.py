from flask import Flask
from app.config import Config
from app.extensions import db, migrate, jwt
from app.models import User, Lead, Message
from app.routes.auth_routes import auth_bp
from app.routes.lead_routes import lead_bp
from app.routes.message_routes import message_bp
from app.routes.analytics_routes import analytics_bp # 1. Importar o novo Blueprint

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # 2. Registrar os Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(lead_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(analytics_bp) # 3. Registrar o Analytics

    @app.route('/health')
    def health_check():
        return {"status": "online", "project": "DevConnect CRM"}, 200

    return app