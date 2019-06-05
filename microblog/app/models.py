from datetime import datetime
from app import db

# this class inherits from db.Model, a base class
class User(db.Model):
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
