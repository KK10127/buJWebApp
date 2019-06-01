from flask import Flask
from config import Config

# importing things needed for db and migration engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

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

from app import routes, models
