# DevConnect CRM 🚀  
### API de Networking Ético para Desenvolvedores

DevConnect CRM é uma **API RESTful desenvolvida em Python** com o objetivo de ajudar **desenvolvedores iniciantes** a organizar, priorizar e personalizar abordagens de networking profissional no LinkedIn **de forma ética, manual e estratégica**.

O projeto funciona como um **CRM de networking**, permitindo gerenciar potenciais contatos (leads), gerar mensagens personalizadas e acompanhar o progresso das interações — **sem violar os Termos de Uso do LinkedIn**.

---

## 🎯 Motivação

Muitos desenvolvedores júnior enfrentam dificuldades como:

- Não saber quem abordar primeiro
- Enviar mensagens genéricas
- Falta de organização no networking
- Ausência de acompanhamento (follow-up)

O DevConnect CRM resolve esse problema ao fornecer uma **estrutura clara e profissional de networking**, baseada em priorização e personalização.

---

## ⚠️ Aviso Importante (Ética e Legalidade)

Este projeto **NÃO**:
- Faz scraping do LinkedIn
- Envia convites automaticamente
- Envia mensagens automáticas
- Simula comportamento de navegador ou usuário

✅ Todos os dados são inseridos **manualmente**  
✅ As mensagens são **geradas**, mas **enviadas manualmente pelo usuário**  
✅ O foco é **organização, inteligência e apoio à decisão**

Este projeto foi desenhado intencionalmente para **respeitar políticas de plataformas e boas práticas profissionais**.

---

## 🎓 Objetivo Educacional e de Portfólio

Este projeto foi desenvolvido com foco em portfólio profissional, demonstrando domínio prático em:

-Desenvolvimento backend com Python

-Criação de APIs REST profissionais

-Modelagem de dados relacional

-Arquitetura de software em camadas

-Implementação de regras de negócio reais

-Automação ética

-Progamação Orientada a Objetos(POO)

## 🧠 O que o projeto faz

- Gerencia potenciais contatos profissionais (leads)
- Classifica e prioriza contatos automaticamente (scoring)
- Gera mensagens personalizadas de conexão
- Organiza o pipeline de networking
- Funciona como um CRM focado em carreira tech

---

## 🧩 Funcionalidades (MVP)

### 🔐 Autenticação
- Cadastro de usuário
- Login com JWT

### 👤 Gestão de Leads
- Criar, editar e listar leads
- Classificar por stack, senioridade e status
- Atualizar status do contato

### 🧠 Scoring Inteligente
Cada lead recebe um **score automático**, baseado em:
- Stack (Python, Backend)
- Cargo (Dev, Tech Lead, etc.)
- Senioridade
- Localização (Brasil)

Isso ajuda a responder:
> “Quem devo abordar primeiro?”

---

### ✉️ Geração de Mensagens
Mensagens personalizadas são geradas com base no perfil do lead, prontas para **copiar e colar manualmente no LinkedIn**.

Exemplo:

> Olá Ana, tudo bem?  
>  
> Sou estudante de Python com foco em desenvolvimento backend e APIs REST. Tenho estudado Flask, bancos de dados relacionais e boas práticas de arquitetura.  
>  
> Vi que você atua como Backend Developer e seria uma honra fazer parte do seu ciclo de conexões e aprender com sua experiência.  
>  
> Obrigado pelo seu tempo!

---

### 🔄 Pipeline de Networking

Cada lead passa por um fluxo claro:

- novo  
- mensagem_gerada  
- convite_enviado  
- aceito  
- respondeu  
- arquivado  

Isso permite acompanhamento real, como em CRMs profissionais.

---

## 🧱 Arquitetura do Projeto

- API REST
- Arquitetura em camadas
- Separação clara de responsabilidades
- Regras de negócio isoladas
- Código orientado a objetos (POO)

---


## 🗂️ Estrutura de Pastas
devconnect-crm/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   │   ├── user.py
│   │   ├── lead.py
│   │   ├── message.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── lead_service.py
│   │   ├── scoring_service.py
│   │   ├── message_generator.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   ├── lead_routes.py
│   │   ├── message_routes.py
│   ├── utils/
│   │   ├── validators.py
│   │   ├── templates.py
├── migrations/
├── tests/
├── run.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md

--

## 🛠️ Tecnologias Utilizadas

-Python

-Flask

-Flask-JWT-Extended

-Flask-SQLAlchemy

-Flask-Migrate

-MySQL

-PyMySQL

-bcrypt

-python-dotenv