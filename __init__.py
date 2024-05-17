from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mykey'
app.config['MAIL_SERVER']= "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "pythonuserflask@gmail.com"
app.config['MAIL_PASSWORD'] =  "gurs szsm zbrh cljb"
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

from . import routes