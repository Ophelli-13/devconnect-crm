from app.models.lead import Lead
from app.models.message import Message
from app.extensions import db
# Supondo que você criou o scoring_service.py
from app.services.scoring_service import ScoringService 

class LeadService:
    @staticmethod
    def create_lead(data, user_id):
        # Implementa o "Scoring Automático" citado no README
        calculated_score = ScoringService.calculate_score(data)
        
        new_lead = Lead(
            name=data.get('name'),
            email=data.get('email'),
            company=data.get('company'),
            role=data.get('role'),
            score=calculated_score,
            user_id=user_id,
            status='novo'
        )
        db.session.add(new_lead)
        db.session.commit()
        return new_lead

    @staticmethod
    def get_prospecting_summary(user_id):
        """Retorna visão clara para gestão do fluxo (Prospects)"""
        results = db.session.query(Lead, Message).\
            join(Message, Lead.id == Message.lead_id).\
            filter(Lead.user_id == user_id).\
            order_by(Lead.score.desc()).all() # Prioriza os de maior score
        
        return [{
            "lead_id": lead.id,
            "lead_name": lead.name,
            "score": lead.score,
            "company": lead.company,
            "current_status": lead.status,
            "message_id": message.id,
            "message_status": message.status
        } for lead, message in results]