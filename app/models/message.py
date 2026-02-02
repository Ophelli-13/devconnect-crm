import uuid
from app.extensions import db
from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    lead_id = db.Column(db.String(36), db.ForeignKey('leads.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)