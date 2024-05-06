from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from flask_session import Session
import uuid

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'
app.config['SECRET_KEY'] = 'mykey'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#Email Configuration
mail = Mail(app)
app.config['MAIL_SERVER']="live.smtp.mailtrap.io"
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "api"
app.config['MAIL_PASSWORD'] = "0469d4f1cf2bb55c5ee45c43e50321c9"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_fName = db.Column(db.String(200), nullable=False)
    user_lName = db.Column(db.String(200), nullable=False)
    user_email = db.Column(db.String(200), nullable=False, unique =True)
    user_pswd = db.Column(db.String(200), nullable=False)
    user_token = db.Column(db.String(1000), nullable=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
        
app.app_context().push()
db.create_all()

@app.route("/")
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email = form.Email.data).first()
        if user:
            #session['user_name'] = User['user_fName'] + ' ' + User['user_lName']
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
                return render_template ('login.html', form=form)
        
    return render_template ('register.html', form=form)

@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    allusers = User.query.all()
    print (allusers)
    return render_template ('home.html', users = allusers)

@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        my_data = User.query.get(request.form.get('id'))
        
        my_data.user_fName = request.form['firstname']
        my_data.user_lName = request.form['lastname']
        my_data.user_email = request.form['email']

        db.session.commit()
        flash("User updated successfully", "success")

    return redirect(url_for('home'))

@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):    
    my_data = User.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("User deleted successfully", "success")   
    return redirect(url_for('home'))

@app.route('/email/<emailID>/', methods = ['GET', 'POST'])
def email(emailID):
    message = Message(
                        subject = 'Hello', 
                        sender =   'mailtrap@demomailtrap.com', 
                        recipients = [emailID]
                        )
    message.body = "This is a test to " + emailID
    mail.send(message)
    flash("Email sent successfully.", 'success')
    return redirect(url_for('home'))            

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        upload = Upload(eventid='0', filename=file.filename, file = file.read())
        db.session.add(upload)
        db.session.commit()
        flash("File uploaded successfully", "success")
        #return f'Uploaded: {file.filename}'
    return render_template ('Upload.html')

@app.route('/resetrequest', methods = ['GET', 'POST'])
def resetrequest():
    form = ResetRequestForm()

    if form.validate_on_submit():  
        user = User.query.filter_by(user_email=form.Email.data).first()
        if user:
            x = uuid.uuid1()
            uid = (uuid.uuid5(x,form.Email.data))
            _sendEmail = sendemail(user.id, user.user_email, str(uid))
            if _sendEmail == '1':

                flash("Thank you for providing your email address. We'll send you a verification code shortly.", "success")
                return render_template ('changepassword.html', form=form)
                
    return render_template ('resetrequest.html', form=form)

@app.route('/changepassword', methods = ['GET', 'POST'])
def changepassword():
    form = ChangePasswordForm()

    if form.validate_on_submit(): 
        user = User.query.filter_by(user_email=form.Email.data).first()
        if user.user_token == form.UserToken.data:
            if form.Password.data == form.ConfirmPassword.data:
                
                hashed_password = generate_password_hash(form.Password.data, method='pbkdf2:sha256')
                user.user_pswd = hashed_password
                user.user_token = None
                db.session.commit()

                flash("Password has been reset successfully.", "success")
                return render_template ('login.html', form=form)
            else:
                flash("Passwords do not match.", "error")
        else:   
            flash("Invalid Token, please re-enter.", "error")                
    return render_template ('changepassword.html', form=form)
    
def sendemail(userid, email, uid):
    message = Message(
                        subject = 'Hello', 
                        sender =   'mailtrap@demomailtrap.com', 
                        recipients = [email]
                        )
    message.body = "<table cellpadding='0' cellspacing='0' width='100%' bgcolor='#fafafa' style='background-color: #fafafa; border-radius: 10px; border-collapse: separate;font-size:18px; color:grey; font-family:calibri'><tbody class='ui-droppable'><tr class='ui-draggable'><td align='left' class='esd-block-text es-p20 esd-frame esd-hover esd-draggable esd-block esdev-enable-select' esd-handler-name='textElementHandler'><div class='esd-block-btn esd-no-block-library'><div class='esd-more'><a><span class='es-icon-dot-3'></span></a></div><div class='esd-move ui-draggable-handle' title='Move'><a><span class='es-icon-move'></span></a></div><div class='esd-copy ui-draggable-handle' title='Copy'><a><span class='es-icon-copy'></span></a></div><div class='esd-delete' title='Delete'><a><span class='es-icon-delete'></span></a></div></div><h3>Welcome,&nbsp;</h3><p><br></p><p style=''>You're receiving this message because you recently reset your password&nbsp;for a account.<br><br>Please copy the below token and confirm your email address for resetting your password. This step adds extra security to your business by verifying the token and email.</p>    <br></td></tr><tr><td>This is your token password reset token:</td></tr><tr><td><b>"+ uid + "</b></td></tr></tbody></table>"    
    message.html = message.body
    mail.send(message)

    my_data = User.query.get(userid)        
    my_data.user_token = uid
    db.session.commit()
    
    return '1'  

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash ("Logged Out Successfully", "success")
    return redirect('/')

if __name__ == "__main__":
     app.run(debug=True)
