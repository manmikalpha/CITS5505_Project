from flask import Flask
from models import db,Events,Images
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
app.app_context().push()
db.create_all()
# db.drop_all( )


