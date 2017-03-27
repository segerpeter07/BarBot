"""
Simple "Hello, World" application using Flask
"""

import os
from flask import Flask
from flask import render_template
from flask import request
app = Flask('flaskapp')


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index.html')


@app.route('/hello/', methods=['GET', 'POST'])
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/login', methods=['GET'])
def login():
    if 'GET':
        return render_template('login.html')
    else:
        return render_template('hello.html')


@app.route('/profile?firstname=Peter&lastname=Seger', methods=['GET', 'POST'])
def dashboard():
    return request.method


@app.route('/profile', methods=['POST', 'GET'])
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
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
