"""
Simple "Hello, World" application using Flask
"""

from flask import Flask
from flask import render_template
from flask import request
from tester1 import*
flask_app = Flask('flaskapp')


@flask_app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')


@flask_app.route('/admin', methods=['GET', 'POST'])
def do_me():
    run_admin()


@flask_app.route('/hello/', methods=['GET', 'POST'])
@flask_app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@flask_app.route('/login', methods=['GET'])
def login():
    if 'GET':
        return render_template('login.html')
    else:
        return render_template('hello.html')


@flask_app.route('/profile?firstname=Peter&lastname=Seger', methods=['GET', 'POST'])
def dashboard():
    return request.method


@flask_app.route('/profile', methods=['POST', 'GET'])
def profile():
    # return request.method
    firstname = request.form.get('firstname')
    return firstname
    # return firstname
    # lastname = request.form['lastname']
    # return(firstname + '  ' + lastname)
    # if len(firstname) != 0 and len(lastname) != 0:
    #     return render_template('profile.html')
    # else:
    #     return render_template('redirect.html')


# app = flask_app.wsgi_app

if __name__ == '__main__':
    flask_app.run()
