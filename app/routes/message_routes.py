from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.services.message_service import MessageService

message_bp = Blueprint('messages', __name__, url_prefix='/messages')

@message_bp.route('/generate/<lead_id>', methods=['POST'])
@jwt_required()
def generate(lead_id):
    response, status = MessageService.generate_connection_message(lead_id)
    return jsonify(response), status