from flask import Flask
from .models import db
from .config import Config
from flask_mail import Mail
from .routes import *
from . import app

app.config['SECRET_KEY'] = 'mykey'
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()
db.create_all()
# db.drop_all( )

#Email Configuration
mail = Mail(app)
app.config['MAIL_SERVER']= "smtp.gmail.com"# "live.smtp.mailtrap.io"
app.config['MAIL_PORT'] = 465 #587
app.config['MAIL_USERNAME'] = "pythonuserflask@gmail.com"#"api"
app.config['MAIL_PASSWORD'] =  "gurs szsm zbrh cljb" #"0469d4f1cf2bb55c5ee45c43e50321c9"
#app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)



