from flask import Flask

app = Flask(__name__)

# Specifying configuration options
# I will enforce the principle of 'seperation of concerns'
# so instead of putting my configuration in the same place where I
# create my application I will use a slightly more elaborate structure
# that allows me to keep my configuration in a seperate file.
#
# I will use a class for this
app.config['SECRET_KEY'] = 'you-will-never-guess'

# add more variables here as needed

from app import routes
