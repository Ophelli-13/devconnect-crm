from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.lead_service import LeadService

lead_bp = Blueprint('leads', __name__, url_prefix='/leads')

@lead_bp.route('/prospects', methods=['GET'])
@jwt_required()
def list_prospects():
    # Esta rota resolve o problema dos IDs que você mencionou
    user_id = get_jwt_identity()
    summary = LeadService.get_prospecting_summary(user_id)
    return jsonify(summary), 200

@lead_bp.route('/', methods=['POST'])
@jwt_required()
def create_lead():
    user_id = get_jwt_identity()
    data = request.get_json()
    lead = LeadService.create_lead(data, user_id)
    return jsonify({"id": lead.id, "score": lead.score}), 201