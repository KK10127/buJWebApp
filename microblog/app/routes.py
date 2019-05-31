from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
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
    return render_template('index.html', title = 'Home',
        user = user, posts = posts)

# This tells Flask that this view function accepts GET and POST requests,
# overriding the default, which is to accept only GET requests.
@app.route('/login', methods=['GET', 'POST'])
def login():
    # creating a form object
    form = LoginForm()

    # when the browser sends the GET request to recieve the web page with the
    # form, this method is going to return False, so that in that case the
    # function skips this 'if' statement and goes directly to render the
    # template in the last line of the function
    if form.validate_on_submit():

        # the flash() function is a useful way to show a message to the user.
        # alot of applications use this technique to let the user know if some
        # action has been successful or not.
        flash('Login requested for user {}, remember_me = {}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title = 'Sign In', form = form)
