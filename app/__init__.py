from flask import Flask
from flask_mail import Mail
from .config import Config
from .models import db
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()
db.create_all()
# db.drop_all( )
app.config['SECRET_KEY'] = 'mykey'
app.config['MAIL_SERVER']= "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "pythonuserflask@gmail.com"
app.config['MAIL_PASSWORD'] =  "gurs szsm zbrh cljb"
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

def create_app(config):
    flaskApp = Flask(__name__)
    flaskApp.config.from_object(config)
    db.init_app(flaskApp)
    return flaskApp

from app import routes
if __name__ == '__main__':
    app.run(debug=True)
