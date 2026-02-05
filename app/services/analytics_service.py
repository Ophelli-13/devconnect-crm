from app.models.lead import Lead
from app.models.message import Message
from sqlalchemy import func
from app.extensions import db

class AnalyticsService:
    @staticmethod
    def get_main_stats(user_id):
        # Contagem total por status de Lead
        stats = db.session.query(
            Lead.status, func.count(Lead.id)
        ).filter_by(user_id=user_id).group_by(Lead.status).all()

        # Transformar em dicionário para facilitar o Front-end
        stats_dict = dict(stats)

        # Média de Score dos leads atuais
        avg_score = db.session.query(func.avg(Lead.score)).filter_by(user_id=user_id).scalar() or 0

        return {
            "total_leads": sum(stats_dict.values()),
            "by_status": {
                "novo": stats_dict.get('novo', 0),
                "mensagem_gerada": stats_dict.get('mensagem_gerada', 0),
                "contatado": stats_dict.get('contatado', 0),
                "aceito": stats_dict.get('aceito', 0)
            },
            "average_lead_quality": round(float(avg_score), 2),
            "conversion_rate": f"{round((stats_dict.get('contatado', 0) / sum(stats_dict.values()) * 100), 1)}%" if sum(stats_dict.values()) > 0 else "0%"
        }