import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # The configuration settings are defined as class variables inside the
    # Config class. As the application needs more configuration items, they
    # will be added to this class. Later, if I find that I need to have more
    # than one configuration set, I can create subclasses of it.

    # Here im taking the database URL from the DATABASE_URL environment variable
    # and if that isnt defined, I'm configuring a database named app.db located
    # in the main directory of the application, which is stored in the basedir
    # variable.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir,'app.db')

    # This is set to False to disable a feature of Flask-SQLAlchemy that I do
    # not need, which is to signal the application every time a change is about
    # to be made in the database.git
    SQLALCHEMY_TRACK_MODIFICATIONS = False
