from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models.message import Message
from app.models.lead import Lead
from app.extensions import db

message_bp = Blueprint('messages', __name__, url_prefix='/messages')

@message_bp.route('/<string:message_id>/status', methods=['PATCH'])
@jwt_required()
def update_workflow(message_id):
    
    data = request.get_json()
    new_status = data.get('status') # ex: 'enviada', 'aceito', 'respondeu'
    
    message = Message.query.get(message_id)
    if not message:
        return jsonify({"error": "Mensagem não encontrada"}), 404
    
    message.status = new_status
    
    # Sincroniza o status do Lead com o pipeline do README
    lead = Lead.query.get(message.lead_id)
    if lead:
        # Mapeamento de status: se a msg foi enviada, o lead foi contatado
        if new_status == 'enviada':
            lead.status = 'convite_enviado'
        elif new_status == 'aceito':
            lead.status = 'aceito'
            
    db.session.commit()
    return jsonify({
        "msg": "Pipeline atualizado",
        "lead_status": lead.status,
        "message_status": message.status
    }), 200