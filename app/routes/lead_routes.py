from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.lead_service import LeadService
from app.models.lead import Lead
from app.extensions import db

lead_bp = Blueprint('leads', __name__, url_prefix='/leads')

@lead_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    user_id = get_jwt_identity()
    data = request.get_json()
    response, status = LeadService.create_lead(user_id, data)
    return jsonify(response), status

@lead_bp.route('/', methods=['GET'])
@jwt_required()
def list_leads():
    user_id = get_jwt_identity()
    response, status = LeadService.get_user_leads(user_id)
    return jsonify(response), status

@lead_bp.route('/<lead_id>', methods=['PATCH'])
@jwt_required()
def update_status(lead_id):
    data = request.get_json()
    new_status = data.get('status')
    
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({"error": "Lead não encontrado"}), 404
        
    lead.status = new_status
    db.session.commit()
    
    return jsonify({"message": f"Status atualizado para {new_status}"}), 200