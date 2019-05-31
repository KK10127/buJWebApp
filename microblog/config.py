import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # The configuration settings are defined as class variables inside the
    # Config class. As the application needs more configuration items, they
    # will be added to this class. Later, if I find that I need to have more
    # than one configuration set, I can create subclasses of it.
