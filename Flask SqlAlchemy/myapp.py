from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SECRET_KEY'] = 'mykey'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_fName = db.Column(db.String(200), nullable=False)
    user_lName = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(200), nullable=False, unique =True)
    user_pswd = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    Email = StringField(validators=[InputRequired(), Email(message ='Please enter a valid email.'), Length(min=4, max=200)], render_kw={"placeholder": "Email"})
    Password = PasswordField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Password"})

class RegistrationForm(FlaskForm):
    FirstName = StringField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "First Name"})
    LastName = StringField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Last Name"})
    Email = StringField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Email"})
    Password = PasswordField(validators=[InputRequired(), Length(min=4, max=200)], render_kw={"placeholder": "Password"})
        
app.app_context().push()
db.create_all()

@app.route("/")
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email = form.Email.data).first()
        if user:
            #if user.user_pswd == form.Password.data:
            if check_password_hash(user.user_pswd, form.Password.data):
                login_user(user, remember='')
                return redirect(url_for('home'))
            else: 
                flash("Password does not match, please re-enter again.", "error")         
        else:
            flash("User not found. Please register to gain access.", "error")
    return render_template ('login.html', form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():        
        existing_useremail = User.query.filter_by(user_email = form.Email.data).first()
        hashed_password = generate_password_hash(form.Password.data, method='pbkdf2:sha256')

        if existing_useremail:
            if existing_useremail.user_email != form.Email.data:                
                new_user = User(user_fName = form.FirstName.data, user_lName = form.LastName.data, user_email = form.Email.data, user_pswd = hashed_password)
                db.session.add(new_user)
                db.session.commit()
            else: 
                flash("User with email " + form.Email.data + " already exists. Please choose a different email.", "error")
        else:
            if existing_useremail is None:
                new_user = User(user_fName = form.FirstName.data, user_lName = form.LastName.data, user_email = form.Email.data, user_pswd = hashed_password)
                db.session.add(new_user)
                db.session.commit()
                flash ("New User " + form.FirstName.data + " " + form.LastName.data + " created Successfully", "success")
        
    return render_template ('register.html', form=form)

@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    return render_template ('home.html', name = current_user.user_fName + ' ' + current_user.user_lName)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash ("Logged Out Successfully", "success")
    return redirect('/')

if __name__ == "__main__":
     app.run(debug=True)