from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def register_user(data):
        email = data.get('email')
        name = data.get('name')
        password = data.get('password')

        if not email or not name or not password:
            return {"error": "Nome, email e senha são obrigatórios"}, 400

        if User.query.filter_by(email=email).first():
            return {"error": "Este email já está em uso"}, 400
        
        try:
            new_user = User(
                name=name,
                email=email
            )
            new_user.set_password(password)
            
            db.session.add(new_user)
            db.session.commit()
            
            return {
                "message": "Usuário registrado com sucesso",
                "user": {
                    "id": new_user.id,
                    "name": new_user.name,
                    "email": new_user.email
                }
            }, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Erro ao criar usuário: {str(e)}"}, 500

    @staticmethod
    def login_user(data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"error": "Email e senha são obrigatórios"}, 400

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            
            access_token = create_access_token(identity=user.id)
            return {
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email
                }
            }, 200
            
        return {"error": "E-mail ou senha incorretos"}, 401