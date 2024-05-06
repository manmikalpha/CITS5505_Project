from flask_sqlalchemy import SQLAlchemy
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
        return f"Events('{self.title}', '{self.date}', '{self.description}', '{self.image}', '{self.prize}', '{self.participants}', '{self.date_created}')"

