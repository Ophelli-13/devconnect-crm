import uuid
from app.extensions import db
from datetime import datetime

class Lead(db.Model):
    __tablename__ = 'leads'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    linkedin_url = db.Column(db.String(255))
    role = db.Column(db.String(100))
    company = db.Column(db.String(100))
    country = db.Column(db.String(50), default='Brasil')
    seniority = db.Column(db.String(50))
    score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='novo')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship('Message', backref='lead', lazy=True, cascade="all, delete-orphan")