from flask import render_template, request, Response, jsonify, redirect, url_for, flash, redirect, abort
import os
from .models import db, Events,Images, User, Upload, LoginForm, RegistrationForm, ResetRequestForm, ChangePasswordForm
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message
from flask_session import Session
import uuid
from .app import app, mail
from datetime import datetime
from flask_uploads import UploadSet, configure_uploads, IMAGES
# pip install email_validator
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)


class FooException(Exception):
    """ Binds optional status code and encapsulates returing Response when error is caught """
    def __init__(self, *args, **kwargs):
        code = kwargs.pop('code', 400)
        Exception.__init__(self)
        self.code = code

    def as_http_error(self):
        return Response(str(self), self.code)

@app.route("/")
@app.route('/login', methods = ['GET', 'POST'])
def login():
    try:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(user_email = form.Email.data).first()
            if user:
                if check_password_hash(user.user_pswd, form.Password.data):
                    login_user(user, remember='')
                    return render_template ('home.html', legend=user.user_fName + ' ' + user.user_lName)
                else: 
                    flash("Password does not match, please re-enter again.", "error")         
            else:
                flash("User not found. Please register to gain access.", "error")
        return render_template ('login.html', form=form)
    except Exception as e:
        flash(str(e), "error")
        return render_template('login.html', form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    try:
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
    except Exception as e:
        flash(str(e), "error")
        return render_template('register.html', form=form)


@app.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    try:
        allusers = User.query.all()
        print (allusers)
        return render_template ('home.html', users = allusers)
    except Exception as e:
        flash(str(e), "error")
        return render_template('home.html')

@app.route('/update', methods = ['GET', 'POST'])
def update():
    try:
        if request.method == 'POST':
            my_data = User.query.get(request.form.get('id'))            
            my_data.user_fName = request.form['firstname']
            my_data.user_lName = request.form['lastname']
            my_data.user_email = request.form['email']

            db.session.commit()
            flash("User updated successfully", "success")

        return redirect(url_for('home'))
    except Exception as e:
        flash(str(e), "error")


@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):    
    try:
        my_data = User.query.get(id)
        db.session.delete(my_data)
        db.session.commit()
        flash("User deleted successfully", "success")   
        return redirect(url_for('home'))
    except Exception as e:
        flash(str(e), "error")

@app.route('/email/<emailID>/', methods = ['GET', 'POST'])
def email(emailID):
    try:
        message = Message(
                            subject = 'Hello', 
                            sender =   'pythonuserflask@gmail.com', 
                            recipients = [emailID]
                            )        
        message.body = "This is a test to " + emailID
        mail.send(message)
        flash("Email sent successfully.", 'success')
        return redirect(url_for('home')) 
    except Exception as e:
        flash(str(e), "error")           

@app.route('/upload', methods = ['GET', 'POST'])
def upload():
    try:
        if request.method == 'POST':
            file = request.files['file']
            upload = Upload(eventid='0', filename=file.filename, file = file.read())
            db.session.add(upload)
            db.session.commit()
            flash("File uploaded successfully", "success")
            #return f'Uploaded: {file.filename}'
        return render_template ('Upload.html')
    except Exception as e:
        flash(str(e), "error")

@app.route('/resetrequest', methods = ['GET', 'POST'])
def resetrequest():
    try:
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
    except Exception as e:
        flash(str(e), "error")
        return render_template('resetrequest.html', form=form)

@app.route('/changepassword', methods = ['GET', 'POST'])
def changepassword():
    try:
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
    except Exception as e:
        flash(str(e), "error")
    
def sendemail(userid, email, uid):
    try:
        user = User.query.filter_by(id=userid).first()
        message = Message(
                         subject = 'Password Reset Token', 
                         sender =   'pythonuserflask@gmail.com',#'mailtrap@demomailtrap.com', 
                         recipients = [email]
                         )
        message.body = "<table cellpadding='0' cellspacing='0' width='100%' bgcolor='#fafafa' style='background-color: #fafafa; border-radius: 10px; border-collapse: separate;font-size:18px; color:grey; font-family:calibri'><tbody class='ui-droppable'><tr class='ui-draggable'><td align='left' class='esd-block-text es-p20 esd-frame esd-hover esd-draggable esd-block esdev-enable-select' esd-handler-name='textElementHandler'><div class='esd-block-btn esd-no-block-library'><div class='esd-more'><a><span class='es-icon-dot-3'></span></a></div><div class='esd-move ui-draggable-handle' title='Move'><a><span class='es-icon-move'></span></a></div><div class='esd-copy ui-draggable-handle' title='Copy'><a><span class='es-icon-copy'></span></a></div><div class='esd-delete' title='Delete'><a><span class='es-icon-delete'></span></a></div></div><h3>Welcome &nbsp;" + user.user_fName + " " + user.user_lName +",</h3><p><br></p><p style=''>You're receiving this message because you recently reset your password&nbsp;for a account.<br><br>Please copy the below token and confirm your email address for resetting your password. This step adds extra security to your business by verifying the token and email.</p>    <br></td></tr><tr><td>This is your password reset token:<br></td></tr><tr><td><b>"+ uid + "</b></td></tr></tbody></table>"    
        message.html = message.body
        mail.send(message)

        my_data = User.query.get(userid)        
        my_data.user_token = uid
        db.session.commit()
        return '1'    
    except Exception as e:
        flash(str(e), "error") 
    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash ("Logged Out Successfully", "success")
    return redirect('/')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500
       

@app.route('/events')
@login_required
def events():
    images = Images.query.all()
    events = Events.query.all()  # query all events from the database
    for event in events:
        event.active = True if event.date >= datetime.now() else False
        event.date = event.date.strftime('%d %B %Y')  # change date format to date month year
        event.date_created = event.date_created.strftime('%d %B %Y')
        
    
    return render_template('events.html', events=events, images=images)  # pass the events to the template

@app.route('/create_event' , methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        owner = current_user.user_email
        title = request.form['title']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        description = request.form['description']
        image = (photos.save(request.files['image']))
        participants = 0
        date_created = datetime.now()
        event = Events(owner=owner, title=title, date=date, description=description, image=image, participants=participants, date_created=date_created)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('events.html', title='Create Event')

@app.route('/participate_event/<int:event_id>', methods=['POST'])
def participate_event(event_id):
    event = Events.query.get(event_id)
    event.participants += 1
    save = photos.save(request.files['image'])
    likes = 0
    user_email = current_user.user_email
    date_created = datetime.now()
    image = Images(event_id=event_id, image_name=save, user_email=user_email, likes=likes, date_created=date_created)
    db.session.add(image)
    db.session.commit()
    return redirect(url_for('events'))

@app.route('/get_events')
def get_events():
    type = request.args.get('type')
    if type == 'past':
        events = Events.query.filter(Events.date <= datetime.now()).all()
    elif type == 'current':
        events = Events.query.filter(Events.date > datetime.now()).all()
    else:
        events = Events.query.all()
    return jsonify([event.to_dict() for event in events])

@app.route('/update_likes/<image>/<action>', methods=['POST'])
def update_likes(image, action):
    image = Images.query.get(image)
    if action == 'like':
        image.likes += 1
    else:
        image.likes -= 1
    db.session.commit()
    return redirect(url_for('events'))

@app.route('/get_my_events')
def get_my_events():
    owner = current_user.user_email
    events = Events.query.filter_by(owner=owner).all()
    return jsonify([event.to_dict() for event in events])

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Events.query.get(event_id)
    if request.method == 'POST':
        event.title = request.form['editTitle']
        event.date = datetime.strptime(request.form['editDate'], '%Y-%m-%d').date()
        event.description = request.form['editDescription']
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('events.html', event=event)

@app.route('/delete_event/<int:event_id>', methods=['POST', 'GET'])
def delete_event(event_id):
    images = Images.query.filter_by(event_id=event_id).all()
    for image in images:
        image_path = os.path.join('static', 'img', image.image_name)
        os.remove(image_path)
    Images.query.filter_by(event_id=event_id).delete()
    os.remove(os.path.join('static', 'img', Events.query.get(event_id).image))
    event = Events.query.get(event_id)
    if event is None:
        # Handle the case where the event doesn't exist
        return "Event not found", 404
    if request.method == 'POST':
        db.session.delete(event)
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('404.html')

@app.route('/select_winner/<int:event_id>/<int:image_id>', methods=['POST'])
def select_winner(event_id, image_id):
    event = Events.query.get(event_id)
    if event.owner != current_user.user_email:
        abort(403)  # Forbidden
    event.winner = image_id
    db.session.commit()
    return redirect(url_for('events'))

@app.route('/clear_winner/<int:event_id>', methods=['POST'])
def clear_winner(event_id):
    event = Events.query.get(event_id)
    if event.owner != current_user.user_email:
        abort(403)
    event.winner = None
    db.session.commit()
    return redirect(url_for('events'))

