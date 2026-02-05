from app import create_app
from app.extensions import db
from app.models.lead import Lead
from app.models.message import Message
from app.models.user import User
from app.services.scoring_service import ScoringService
import uuid

def seed_data():
    app = create_app()
    with app.app_context():
        print("🌱 Iniciando o Seeder...")

        # 1. Buscar o primeiro usuário (certifique-se de já ter um user criado)
        user = User.query.first()
        if not user:
            print("❌ Erro: Crie um usuário primeiro pelo /auth/register")
            return

        # 2. Lista de Leads de Exemplo
        leads_data = [
            {"name": "Ana Silva", "role": "Tech Recruiter", "company": "Google"},
            {"name": "Carlos Souza", "role": "Engineering Manager", "company": "Meta"},
            {"name": "Beatriz Oliveira", "role": "Senior Python Developer", "company": "Amazon"},
            {"name": "Ricardo Santos", "role": "Backend Engineer", "company": "Startup X"},
            {"name": "Mariana Costa", "role": "Head of Engineering", "company": "Netflix"}
        ]

        status_options = ['novo', 'mensagem_gerada', 'contatado', 'aceito']
        
        for i, data in enumerate(leads_data):
            # Calcular Score usando o seu ScoringService
            score = ScoringService.calculate_score(data)
            
            # Criar Lead
            new_lead = Lead(
                name=data['name'],
                role=data['role'],
                company=data['company'],
                score=score,
                user_id=user.id,
                status=status_options[i % len(status_options)]
            )
            db.session.add(new_lead)
            db.session.flush() # Para pegar o ID do lead antes do commit

            # Se o status não for 'novo', criar uma mensagem vinculada
            if new_lead.status != 'novo':
                msg_status = 'enviada' if new_lead.status in ['contatado', 'aceito'] else 'rascunho'
                new_msg = Message(
                    lead_id=new_lead.id,
                    content=f"Olá {new_lead.name}, vi que você atua na {new_lead.company}...",
                    status=msg_status
                )
                db.session.add(new_msg)

        db.session.commit()
        print("✅ Banco de dados populado com sucesso!")

if __name__ == "__main__":
    seed_data()