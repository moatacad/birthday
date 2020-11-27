#3rd party import
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail, Message

from flask_migrate import Migrate

#local importation

import config

#instantiate a Flask app
app = Flask(__name__)

csrf=CSRFProtect(app)
#app.config.from_pyfile('config.py')
app.config.from_object('config.Production')

db = SQLAlchemy(app)

mail=Mail(app)

migrate = Migrate(app,db)
#load the views
from birthdayapp import routes, forms ,models