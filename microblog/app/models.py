from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db, login
from flask_login import UserMixin
from hashlib import md5

@login.user_loader  # this decorator registers the user loaded with Flask-Login
def load_user(id):
    return User.query.get(int(id))

# NOTE: I am not declaring this table as a model, like I did for the
# users and posts tables. Since this is an auxiliary table that has
# no data other than the foreign keys, I created it without an
# associated model class.
followers = db.Table('followers', db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

# this class inherits from db.Model, a base class
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index =True, unique = True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default = datetime.utcnow)

    # Now I declare the many-to-many relationship in the users table
    followed = db.relationship('User', secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy = 'dynamic')

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

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    # this query is beast:
    # Post.query.join(...).filter(...).order_by(...)
    # gets all posts by your followers including your own posts
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


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
