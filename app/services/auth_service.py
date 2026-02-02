from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token

class AuthService:
    @staticmethod
    def register_user(data):
        try:
            email = data.get('email')
            if User.query.filter_by(email=email).first():
                return {"error": "Email já cadastrado"}, 400
            
            new_user = User(
                name=data.get('name'),
                email=email
            )
            new_user.set_password(data.get('password'))
            
            db.session.add(new_user)
            db.session.commit()
            
            return {"message": "Usuário criado com sucesso", "id": new_user.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": f"Erro no registro: {str(e)}"}, 500

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user and user.check_password(data.get('password')):
    
                access_token = create_access_token(identity=str(user.id))
                return {
                    "access_token": access_token,
                    "user": {"id": user.id, "name": user.name}
                }, 200
            return {"error": "Credenciais inválidas"}, 401
        except Exception as e:
            return {"error": f"Erro na criptografia/login: {str(e)}"}, 500