from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from hashlib import md5

@login.user_loader  # this decorator registers the user loaded with Flask-Login
def load_user(id):
    return User.query.get(int(id))

# this class inherits from db.Model, a base class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index =True, unique = True)
    password_hash = db.Column(db.String(128))

    #
    posts = db.relationship('Post', backref ='author',lazy='dynamic')

    # this method tells python how to print objects of this class, which is
    # going to be useful for debugging.
    def __repr__(self):
        return '<User {}>'.format(self.username)

    # with these two methods below in place, a user object is now able to do
    # secure password verification, without the need to ever store orgiginal
    # passwords.
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # this method returns the URL of the user's avatar image, scaled to the
    # requested size in pixels.
    def avatar(self,size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

# The Post class will represent blog posts written by users. The 'timestamp'
# field is going to be idexed, which is useful if I want to retrieve posts in
# chronological order.
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))

    # These timestamps will be converted to the user's local time when they are
    # displayed.
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
