"""
Simple "Hello, World" application using Flask
"""

import os
import time
import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, flash, redirect, render_template, request, session, abort
from database_test import *


app = Flask('flaskapp')


# ------HOME PAGE------->
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
# ---------------------->


# <-----HOME PAGE-------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return render_template('dashboard.html')
# --------------------->
            return render_template('dashboard_test.html')


# <-----LOGOUT PAGE-------
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return render_template('login.html')
# ----------------------->


# -------New User-------->
@app.route('/new_user', methods=['GET'])
def new_user():
    if 'GET':
        return render_template('new_user_creation.html')
# ------------------>


# -----Confirmation Page---->
@app.route('/new_user/confirmation', methods=['GET','POST'])
def confirmation():
    email = request.form['email']
    username = request.form['username']
    phone = request.form['phone']
    password = request.form['password']
    if return_user(username) is None:
        insert_user(email, username, phone, password)
        return render_template('confirmation.html')
    else:
        return render_template('invalid.html')
# ---------------------->


# -----Rest Password Page----->
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    return render_template('reset_password.html')
# ------------------------------->


# ------Password Reset Confirm----->
@app.route('/reset_password/confirmation', methods=['GET', 'POST'])
def confirm_reset():
    username = request.form['username']
    phone = request.form['phone']
    password = request.form['password']
    user = return_user(username)
    if user[3] == phone:
        update_info(username, password)
    return render_template('confirmation.html')
# ------------------------->


# -------Dashboard--------->
@app.route('/user', methods=['POST', 'GET'])
@app.route('/user/<string:firstname>', methods=['POST', 'GET'])
def dashboard(firstname=None):
    username = request.form['username']
    password = request.form['password']
    firstname = username
    # Check if user exists
    if return_user(username) is None:
        return render_template('wrong_password.html')

    # user_pass = return_password(username)
    if chec_password(username, password):
        session['logged_in'] = True
        return render_template('dashboard_test.html', firstname=firstname)
    else:
        return render_template('wrong_password.html')


@app.route('/user/settings', methods=['POST', 'GET'])
def dashboard_settings():
    return render_template('dashboard_settings.html', data=return_user('pseger'))


# BAR SECTION
# ----------------------------------------------->

# ------------Bar Home---->
@app.route('/bar', methods=['GET', 'POST'])
def drinks_home():
    return render_template('drinkbuttons.html')
# ------------------------->


# -------Drink Results------>
@app.route('/drinkresults', methods=['GET', 'POST'])
def drink():
    if request.method == 'POST':
        mixers = request.form['mixers']
        alcohol = request.form['alcohol']
        if mixers and alcohol:
            return render_template('drinksresults.html', mixers=mixers, alcohol=alcohol)
# -------------------------->


# -------User Sync Home----->


@app.route('/barcode', methods=['GET', 'POST'])
def barcode():
    return render_template('barcode.html')


@app.route('/bar', methods=['GET','POST'])
def bar():
    return render_template('drinkbuttons.html')


@app.route('/barcoderesult',methods=['GET', 'POST'])
def barcoderesult():
    if request.method == 'POST':
        barcoderesult = request.form['barcode']
        if barcode:
            sync_user('pseger', barcoderesult)
            write_drink_timestamp(barcoderesult)
            return render_template('barcoderesult.html', barcoderesult=barcoderesult)
# ------------------>

# -------------------------------------------->


@app.route("/chart")
def chart():
    '''
    write_drink_timestamp('suh')
    '''
    st = get_drink_timestamp('assuh')
    print(st)
    times = st
    times = [time.strftime("%D %H:%M:%S", time.gmtime(x)) for x in times]
    print(times)
    labels = times
    values = range(len(times))
    return render_template('LinePlotTemplate.html', values=values, labels=labels)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    # app.run(host=HOST, port=PORT)
    app.run('localhost', port=PORT)
