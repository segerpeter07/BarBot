"""
The webapp for the BarBot
Released under Apache License 2.0

@Authors: Peter Seger, Nathan Lepore, Kian Raissian, Lucky Jordan

For more information, consult http://peterhenryseger.com/BarBot/
"""

import os
import time
import datetime
from flask import Flask
from flask import render_template
from flask import request
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from database_test import *
from flask_debugtoolbar import DebugToolbarExtension
from find_BACS_singleuser import *

app = Flask('flaskapp')


# ------HOME PAGE------->
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    return render_template('about.html')
# ---------------------->


# <-----LOGIN PAGE-------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return redirect('/loginconfirm')
# --------------------->


# <-----LOGIN CONFIRM PAGE-------
@app.route('/loginconfirm', methods=['GET', 'POST'])
def login_confirm():
    username = request.form['username']
    password = request.form['password']
    # Check if user exists
    if return_user(username) is None:
        return render_template('wrong_password.html')
    else:
        # user_pass = return_password(username)
        if check_password(username, password):
            session['logged_in'] = True
            return redirect('/user/%s' % (username))
        else:
            return render_template('wrong_password.html')
# --------------------->


# <-----LOGOUT PAGE-------
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['logged_in'] = False
    return render_template('login.html')
# ----------------------->


# -------New User-------->
@app.route('/new_user', methods=['GET', 'POST'])
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
    height = request.form['height']
    weight = request.form['weight']
    age = request.form['age']
    gender = request.form['gender']
    if return_user(username) is None:
        insert_user(email, username, phone, password, height, weight, age, gender)
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
        update_password(username, password)
    return render_template('confirmation.html')
# ------------------------->


# -------Dashboard--------->
@app.route('/user/<string:username>', methods=['POST', 'GET'])
def dashboard(username):
    return render_template('dashboard_test.html', username=username)


@app.route('/user/<string:username>/settings', methods=['POST', 'GET'])
def dashboard_settings(username):
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        return render_template('dashboard_settings.html', data=return_user(username))


@app.route('/user/<string:username>/settings/confirmation', methods=['POST', 'GET'])
def dashboard_settings_confirmation(username):
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        height = request.form['height']
        weight = request.form['weight']
        age = request.form['age']
        gender = request.form['gender']

        update_settings(email, username, phone, height, weight, age, gender)

        return render_template('dashboard_settings.html', data=return_user(username))


# BAR SECTION
# ----------------------------------------------->

# ------------Bar Home---->
@app.route('/bar', methods=['GET', 'POST'])
def drinks_home():
    return render_template('drinkbuttons.html', barcoderesult=barcoderesult)
# ------------------------->


# -------Drink Results------>
@app.route('/bar/<string:barcode>/drinkresults', methods=['GET', 'POST'])
def drink(barcode):
    if request.method == 'POST':
        mixers = request.form['mixers']
        alcohol = request.form['alcohol']
        if mixers and alcohol:
            update_drink(alcohol)
            update_drink(mixers)
            increase_drink_count(barcode)
            return render_template('drinksresults.html', mixers=mixers, alcohol=alcohol)
        else:
            return redirect(url_for('error'))


@app.route('/error', methods=['GET', 'POST'])
def error():
    if request.method == 'POST':
        return redirect(url_for('bar'))
    return render_template('error.html')
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


@app.route("/chart/<string:username>")
def chart(username):
    party_start = 1493008634.6537
    current_time = 1493026634.7893
    max_disp_num = 1  # maximum number of users to display on graph
    if max_disp_num > 3:  # temporary hack because there are only 3 colors in the colors list
        max_disp_num = 3
    res = find_BACS_singleuser(current_time, party_start, max_disp_num, username)
    values, labels, lines, elements, people_to_disp, colors = res
    return render_template('MultiLinePlot2.html', values=values, labels=labels, lines=lines, elements=elements, people=people_to_disp, colors=colors)



# ------------Party Captain Section---------------------->

# -------New Admin-------->
@app.route('/new_admin', methods=['GET'])
def new_admin():
    if 'GET':
        return render_template('newadmin.html')
# ------------------>


# -----Confirmation Page---->
@app.route('/new_admin/confirmation', methods=['GET','POST'])
def admin_confirmation():
    username = request.form['username']
    password = request.form['password']
    adminpassword = request.form['adminpassword']
    if adminpassword == 'sSJ04HvxWK0K':
        if return_admin(username) is None:
            insert_admin(username, password)
            return render_template('adminlogin.html')
        else:
            return render_template('invalid.html')
    else:
        return "You don't have permission for this"
# ---------------------->


# <-----PC LOGIN PAGE-------
@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_login():
    if 'GET':
        if not session.get('logged_in'):
            return render_template('adminlogin.html')
        else:
            return redirect('/adminloginconfirm')
# --------------------->


# <-----PC LOGIN CONFIRM PAGE-------
@app.route('/adminloginconfirm', methods=['GET', 'POST'])
def admin_login_confirm():
    username = request.form['username']
    password = request.form['password']
    # Check if user exists
    if return_admin(username) is None:
        return render_template('wrong_password.html')
    else:
        # user_pass = return_password(username)
        if check_admin(username, password):
            session['logged_in'] = True
            return redirect('/admin/%s' % (username))
        else:
            return render_template('wrong_password.html')
# --------------------->


# -------Dashboard--------->
@app.route('/admin/<string:username>', methods=['POST', 'GET'])
def pc_dashboard(username):
    return render_template('pcdash.html', firstname=username)


# ------------------------------>



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    # app.run(host=HOST, port=PORT)

    app.debug = False
    # app.debug = False
    toolbar = DebugToolbarExtension(app)

    app.run('localhost', port=PORT)
    # app.run('10.7.12.99', port=PORT)
