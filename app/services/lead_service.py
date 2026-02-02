from app.models.lead import Lead
from app.extensions import db

class LeadService:
    @staticmethod
    def create_lead(user_id, data):
        try:
            new_lead = Lead(
                user_id=user_id,
                name=data.get('name'),
                linkedin_url=data.get('linkedin_url'),
                role=data.get('role'),
                company=data.get('company'),
                country=data.get('country', 'Brasil'),
                seniority=data.get('seniority'),
                status='novo'
            )
            db.session.add(new_lead)
            db.session.commit()
            return {"message": "Lead criado com sucesso", "id": new_lead.id}, 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    @staticmethod
    def get_user_leads(user_id):
        leads = Lead.query.filter_by(user_id=user_id).all()
        return [{
            "id": l.id,
            "name": l.name,
            "company": l.company,
            "status": l.status,
            "created_at": l.created_at.isoformat()
        } for l in leads], 200