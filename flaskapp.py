"""
Simple "Hello, World" application using Flask
"""

import os
from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, flash, redirect, render_template, request, session, abort

app = Flask('flaskapp')


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('home.html')


@app.route('/hello/', methods=['GET', 'POST'])
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/login', methods=['GET'])
def login():
    if 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return render_template('dashboard.html')
    else:
        return render_template('hello.html')


# @app.route('/dashboard', methods=['POST', 'GET'])
# def dashboard(firstname=None):
#     firstname = request.form.get('firstname')
#     # user_route = url_for('dashboard', firstname=firstname)
#     return firstname


@app.route('/user', methods=['POST', 'GET'])
@app.route('/user/<string:firstname>', methods=['POST', 'GET'])
def dashboard(firstname=None):
    if request.form['password'] == 'password' and request.form['firstname'] == 'admin':
        session['logged_in'] = True
        return render_template('dashboard.html', firstname=firstname)
    else:
        return render_template('wrong_password.html')
# @app.route(user_route, methods=['POST', 'GET'])
# def dashboard(firstname=None):
#     # return request.method
#     # firstname = request.form.get('firstname')
#     # # lastname = request.form.get('lastname')
#     # password = request.form.get('password')
#     # return (firstname + '  ' + password)
#     return render_template('dashboard.html', firstname=firstname)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
