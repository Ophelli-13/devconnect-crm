from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    response, status = AuthService.register_user(data)
    return jsonify(response), status

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400
        
    response, status = AuthService.login_user(data)
    return jsonify(response), status