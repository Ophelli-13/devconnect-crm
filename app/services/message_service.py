import os
import re
from google import genai
from google.genai import types
from app.models.lead import Lead
from app.models.message import Message
from app.extensions import db


class MessageService:
    GEMINI_MODEL = os.getenv(
        "GEMINI_MODEL",
        "models/gemini-2.5-flash"
    )

    @staticmethod
    def _clean_message_text(text):
        """
        Limpa o texto removendo quebras de linha múltiplas
        e espaços em excesso, mantendo a estrutura do parágrafo.
        """
        # Substitui múltiplas quebras de linha por um espaço único
        text = re.sub(r'\n+', ' ', text)
        # Remove espaços múltiplos
        text = re.sub(r'\s+', ' ', text)
        # Remove espaços antes de pontuação
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        # Adiciona espaço após pontuação se necessário
        text = re.sub(r'([.,!?;:])(?=[A-Za-z])', r'\1 ', text)
        return text.strip()

    @staticmethod
    def generate_connection_message(lead_id):
        # 1. Buscar lead
        lead = Lead.query.get(lead_id)
        if not lead:
            return {"error": "Lead não encontrado"}, 404

        # 2. API Key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return {"error": "API Key ausente no .env"}, 500

        try:
            # 3. Cliente Gemini
            client = genai.Client(api_key=api_key)
            
            # PROMPT MELHORADO - Mais detalhado e específico
            prompt = f"""
Como especialista em networking profissional, escreva uma mensagem de conexão no LinkedIn que seja:

1. PROFISSIONAL E CORDIAL
2. ESPECÍFICA sobre minhas habilidades técnicas
3. INTERESSANTE para um recrutador
4. COM PERSONALIDADE

MINHAS HABILIDADES TÉCNICAS (para incluir na mensagem):
- Desenvolvedor Backend Python
- Flask e FastAPI para construção de APIs
- Bancos de dados (SQL e NoSQL)
- Automações e scripts Python
- Versionamento com Git e GitHub
- Desenvolvimento de APIs REST
- Boas práticas de código e arquitetura

DADOS DO DESTINATÁRIO:
- Nome: {lead.name}
- Cargo: {lead.role}
- Empresa: {lead.company}

DIRETRIZES:
• Saudação personalizada usando o nome
• Mencionar que conheço/ admiro o trabalho da empresa
• Apresentar minhas principais habilidades técnicas de forma natural
• Expressar interesse em oportunidades ou troca de conhecimento
• Chamada para ação educada

EXEMPLO DE TOM ADEQUADO:
"Olá [Nome]! Como vai? Vi seu perfil como [cargo] na [empresa] e me interessei pela trajetória da empresa. Atuo como Desenvolvedor Backend Python, com experiência em Flask, FastAPI, desenvolvimento de APIs REST, bancos de dados e automações. Gostaria de me conectar para expandir minha rede na área de tecnologia e, quem sabe, trocar experiências sobre o mercado. Seria um prazer!"

REGRAS:
- Formato: Um único parágrafo contínuo
- Tamanho: 250-400 caracteres
- Tom: Profissional mas acessível
- Evite clichês como "gostaria de fazer parte do seu time"

Agora, escreva a mensagem personalizada para {lead.name}:
"""

            # 4. Chamada Gemini
            response = client.models.generate_content(
                model=MessageService.GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,  # Aumentado para mais criatividade
                    top_p=0.95,
                    max_output_tokens=500,  # Aumentado para textos mais completos
                    stop_sequences=["\n\n", "---"]
                )
            )

            # 5. Extrair e limpar resposta
            generated_text = ""
            if hasattr(response, 'candidates') and response.candidates:
                for candidate in response.candidates:
                    if hasattr(candidate, 'content') and candidate.content:
                        for part in candidate.content.parts:
                            if hasattr(part, 'text'):
                                generated_text += part.text
            
            # Fallback para método antigo se necessário
            if not generated_text and hasattr(response, "text"):
                generated_text = response.text
            
            generated_text = generated_text.strip()
            
            # Validação
            if not generated_text:
                return {"error": "IA não retornou texto válido"}, 500
            
            # LIMPEZA DO TEXTO
            generated_text = MessageService._clean_message_text(generated_text)
            
            # VALIDAÇÃO DE CONTEÚDO TÉCNICO
            # Se a mensagem não mencionar habilidades técnicas, adicionar
            technical_keywords = ['Python', 'Flask', 'FastAPI', 'backend', 'API', 'banco de dados', 'Git', 'automação']
            has_technical_content = any(keyword.lower() in generated_text.lower() for keyword in technical_keywords)
            
            if not has_technical_content or len(generated_text) < 200:
                # Mensagem muito curta ou sem conteúdo técnico - complementar
                complement = f" Atuo como Desenvolvedor Backend Python com Flask e FastAPI, desenvolvendo APIs REST, trabalhando com bancos de dados, automações e utilizando Git/GitHub para versionamento. Gostaria de me conectar para expandir minha rede profissional na área de tecnologia."
                generated_text = generated_text.rstrip('.') + complement
            
            # Garantir que termina com ponto
            if not generated_text.endswith(('.', '!', '?')):
                generated_text += '.'

            # 6. Persistência
            new_message = Message(
                lead_id=lead.id,
                content=generated_text,
                status="rascunho"
            )

            lead.status = "mensagem_generated"

            db.session.add(new_message)
            db.session.commit()

            return {
                "lead_name": lead.name,
                "generated_message": generated_text,
                "model_used": MessageService.GEMINI_MODEL,
                "status": "rascunho_salvo"
            }, 201

        except Exception as e:
            db.session.rollback()
            print(f"Erro na integração com Gemini: {str(e)}")
            
            # FALLBACK MELHORADO - Com mais conteúdo técnico
            fallback_message = f"""Olá {lead.name}! Vi seu perfil como {lead.role} na {lead.company} e me interessei pela atuação de vocês no mercado de tecnologia. Atuo como Desenvolvedor Backend Python com experiência em Flask e FastAPI para construção de APIs REST, trabalho com bancos de dados SQL e NoSQL, desenvolvimento de automações e utilizo Git/GitHub para versionamento de código. Gostaria de me conectar para expandir minha rede profissional e, quem sabe, trocar experiências sobre desenvolvimento backend e melhores práticas em Python. Seria um prazer!"""
            
            # Limpar o fallback também
            fallback_message = MessageService._clean_message_text(fallback_message)
            
            new_message = Message(
                lead_id=lead.id,
                content=fallback_message,
                status="rascunho_fallback"
            )
            
            lead.status = "mensagem_generated"
            db.session.add(new_message)
            db.session.commit()
            
            return {
                "lead_name": lead.name,
                "generated_message": fallback_message,
                "model_used": "fallback",
                "status": "rascunho_salvo_fallback",
                "warning": "Usado fallback devido a erro na IA"
            }, 201