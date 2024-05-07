from flask import render_template, request,jsonify, redirect, url_for
from models import db, Events,Images
from app import app
from datetime import datetime
from flask_uploads import UploadSet, configure_uploads, IMAGES
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/')
def index():
    return render_template('home.html', title='Home')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')
@app.route('/events')
def events():
    images = Images.query.all()
    events = Events.query.all()  # query all events from the database
    for event in events:
        event.date = event.date.strftime('%d %B %Y')  # change date format to date month year
        event.date_created = event.date_created.strftime('%d %B %Y')
    
    return render_template('events.html', events=events, images=images)  # pass the events to the template

@app.route('/create_event' , methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        description = request.form['description']
        image = (photos.save(request.files['image']))
        prize = float(request.form['prize'])
        participants = 0
        date_created = datetime.now()
        event = Events(title=title, date=date, description=description, image=image, prize=prize, participants=participants, date_created=date_created)
        db.session.add(event)
        db.session.commit()
        return redirect(url_for('events'))
    return render_template('create_event.html', title='Create Event')

@app.route('/participate_event/<int:event_id>', methods=['POST'])
def participate_event(event_id):
    event = Events.query.get(event_id)
    event.participants += 1
    save = (photos.save(request.files['image']))
    likes = 0
    user_email = request.form['user_email']
    image = Images(event_id=event_id, image_name=save, user_email=user_email, likes=likes)
    

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

if __name__ == '__main__':
    app.run(debug=True)