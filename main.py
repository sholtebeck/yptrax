from flask import Flask, render_template, request
from google.appengine.api import users

app = Flask(__name__)
app.config['DEBUG'] = True

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.

def log_inorout():
    # check for login
    log={'user':'dude', 'url':users.create_login_url(request.url), 'url_link': 'Login' }
    if users.get_current_user():
        log['user'] = users.get_current_user().nickname()
        log['url'] = users.create_logout_url(request.url)
        log['url_link'] = 'Logout'
    return log   


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return render_template('hello.html', title='hello', log=log_inorout())

@app.route('/about')
def about():
    return render_template('about.html', title='about', log=log_inorout())

@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404
