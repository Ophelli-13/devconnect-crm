import os
import google.generativeai as genai
from app.models.lead import Lead
from app.models.message import Message
from app.extensions import db

class MessageService:
    @staticmethod
    def generate_connection_message(lead_id):
        # 1. Busca o Lead no banco
        lead = Lead.query.get(lead_id)
        if not lead:
            return {"error": "Lead não encontrado"}, 404

        # 2. Configura a IA do Google (Gemini)
        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return {"error": "API Key 'GEMINI_API_KEY' não encontrada no .env"}, 500
            
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')

            # 3. Prompt estratégico incluindo SEU PERFIL/Altere como necessário
            prompt = f"""
            Aja como um especialista em networking profissional. 
            Crie uma mensagem de conexão para o LinkedIn com no máximo 280 caracteres.
            
            MEU PERFIL (Remetente):
            - Cargo: Desenvolvedor Junior focado em Backend (Python/Flask)
            - Objetivo: Networking e busca por novas oportunidades de trabalho.

            DADOS DO LEAD (Destinatário):
            - Nome: {lead.name}
            - Cargo: {lead.role}
            - Empresa: {lead.company}
            - Sênioridade: {lead.seniority}
            
            DIRETRIZES DA MENSAGEM:
            - Seja pessoal, direto e honesto.
            - Mencione que sou um desenvolvedor focado em Backend/Python.
            - Demonstre interesse na atuação dele(a) ou da empresa.
            - Não peça emprego diretamente na primeira mensagem, mas mostre-se aberto a conexões no setor.
            - Não use clichês como "espero que esteja bem".
            """

            response = model.generate_content(prompt)
            generated_text = response.text.strip()

            # 4. Salva a mensagem gerada como rascunho no banco
            new_message = Message(
                lead_id=lead_id,
                content=generated_text,
                status='rascunho'
            )
            db.session.add(new_message)
            db.session.commit()
            
            return {
                "lead": lead.name,
                "role": lead.role,
                "my_profile": "Backend Python Junior",
                "message": generated_text,
                "status": "rascunho"
            }, 201

        except Exception as e:
            db.session.rollback()
            return {"error": f"Falha na geração por IA: {str(e)}"}, 500