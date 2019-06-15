from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm

from flask_login import current_user, login_user, logout_user, login_required
from app.models import User

from werkzeug.urls import url_parse

from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}

    posts = [
        {
            'author':{'username' : 'John'},
            'body':'Beautiful day in Portland!'
        },
        {
            'author':{'username':'Susan'},
            'body':'The Avengers movie was so cool!'
        },
        {
            'author':{'username':'Jacob'},
            'body':'I like peanut butter!'
        },
        {
            'author':{'username':'Alyssa'},
            'body':'I\'m a witch'
        },
        {
            'author':{'username':'Mark'},
            'body':'What is this blog?'
        }
    ]
    return render_template('index.html', title = 'Home Page', posts = posts)

# This tells Flask that this view function accepts GET and POST requests,
# overriding the default, which is to accept only GET requests.
@app.route('/login', methods=['GET', 'POST'])
def login():

    # these two lines deal with the weird situation that an already logged in
    # user navigates to the '/login' URL of my app (which is clearly a mistake)
    # so I redirect them to the home page.
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    # creating a form object
    form = LoginForm()

    # when the browser sends the GET request to recieve the web page with the
    # form, this method is going to return False, so that in that case the
    # function skips this 'if' statement and goes directly to render the
    # template in the last line of the function
    if form.validate_on_submit():

        user = User.query.filter_by(username = form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            # the flash() function is a useful way to show a message to the user.
            # alot of applications use this technique to let the user know if some
            # action has been successful or not.
            flash('Invalid username or password!')
            return redirect(url_for('login'))

        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form = form)

# this app decorator has the dynamic component
# <username>. Flask will accept any text in
# that portion of the URL, and will invoke the
# view function with the actual text as an arg.
@app.route('/user/<username>')
@login_required # login must be required to view a profile!
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author':user, 'body':'Test post #1'},
        {'author':user, 'body':'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title = 'Edit Profile', form = form)
