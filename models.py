from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    prize = db.Column(db.Float, nullable=False)
    participants = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f"Event('{self.title}', '{self.date}', '{self.description}', '{self.image}', '{self.prize}', '{self.participants}', '{self.date_created}')"
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'date': self.date.isoformat() if isinstance(self.date, datetime) else None,
            'description': self.description,
            'image': self.image,
            'prize': self.prize,
            'participants': self.participants,
            'date_created': self.date_created.isoformat() if isinstance(self.date_created, datetime) else None,
        }
class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    image_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)