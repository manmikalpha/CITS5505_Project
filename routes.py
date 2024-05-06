from flask import render_template, request, redirect, url_for
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
        participants = 100
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
    user_email = request.form['user_email']
    image = Images(event_id=event_id, image_name=save, user_email=request.form['user_email'])
    db.session.add(image)
    db.session.commit()
    return redirect(url_for('events'))

if __name__ == '__main__':
    app.run(debug=True)