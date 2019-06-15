from flask import Flask
from config import Config
from flask_login import LoginManager

# importing things needed for db and migration engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# for logging errors
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)

login = LoginManager(app)
login.login_view = 'login'

# Specifying configuration options
# I will enforce the principle of 'seperation of concerns'
# so instead of putting my configuration in the same place where I
# create my application I will use a slightly more elaborate structure
# that allows me to keep my configuration in a seperate file.
#
# I will use a class for this

# app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config.from_object(Config)

# setting up db object and migration engine object
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models, errors

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(mailhost=(app.config['MAIL_SERVER'],
            app.config['MAIL_PORT']), fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    # write the log file with the name microblog.log in a 'logs' directory,
    # which I create if it doesn't already exist.
    if not os.path.exists('logs'):
        os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
            backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(messages)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Microblog startup')
