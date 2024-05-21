from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from flask_login import UserMixin
db = SQLAlchemy()


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(100), nullable=False)
    participants = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    winner = db.Column(db.Integer, db.ForeignKey('images.id', use_alter=True),nullable=True)
    
    def __repr__(self):
        return f"Event('{self.title}', '{self.date}', '{self.description}', '{self.image}', '{self.prize}', '{self.participants}', '{self.date_created}')"
    def to_dict(self):
        return {
            'id': self.id,
            'owner': self.owner,
            'title': self.title,
            'date': self.date.isoformat() if isinstance(self.date, datetime) else None,
            'description': self.description,
            'image': self.image,
            'participants': self.participants,
            'date_created': self.date_created.isoformat() if isinstance(self.date_created, datetime) else None,
        }
class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id', use_alter=True), nullable=False)
    image_name = db.Column(db.String(100), nullable=False)
    user_email = db.Column(db.String(100), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)

    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_fName = db.Column(db.String(200), nullable=False)
    user_lName = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(200), nullable=False, unique =True)
    user_pswd = db.Column(db.String(200), nullable=False)
    user_token = db.Column(db.String(1000), nullable=True)




class LoginForm(FlaskForm):
    Email = StringField(validators=[InputRequired(), Email(message ='Please enter valid email address.'), Length(min=4, max=200)], render_kw={"placeholder": "Email"})
    Password = PasswordField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Password"})

class RegistrationForm(FlaskForm):
    FirstName = StringField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "First Name"})
    LastName = StringField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Last Name"})
    Email = StringField(validators=[InputRequired(), Length(min=4, max=200), Email("This field requires a valid email address")], render_kw={"placeholder": "Email"})
    Password = PasswordField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Password"})

class ResetRequestForm(FlaskForm):
    Email = StringField(validators=[InputRequired(), Length(min=4, max=200), Email("Please enter valid email address.")], render_kw={"placeholder": "Email"})
    UserToken = StringField(render_kw={"placeholder": "UserToken"})
    Password = PasswordField(render_kw={"placeholder": "Password"})
    ConfirmPassword = PasswordField(render_kw={"placeholder": "ConfirmPassword"})

class ChangePasswordForm(FlaskForm):
    Email = StringField(validators=[InputRequired(), Length(min=4, max=200), Email("Please enter valid email address.")], render_kw={"placeholder": "Email"})
    Password = PasswordField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Password"})
    ConfirmPassword = PasswordField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "ConfirmPassword"})
    UserToken = StringField(validators=[InputRequired()], render_kw={"placeholder": "UserToken"})

class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventid = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    file = db.Column(db.LargeBinary)
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='questions')
    answers = db.relationship('Answer', backref='question', lazy='dynamic')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref= 'answers')