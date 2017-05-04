"""
The webapp for the BarBot
Released under Apache License 2.0

@Authors: Peter Seger, Nathan Lepore, Kian Raissian, Lucky Jordan

For more information, consult http://peterhenryseger.com/BarBot/
"""

import os
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from database_test import *
from flask_debugtoolbar import DebugToolbarExtension
from find_BACS_singleuser import *
from find_max_BACs import *
import time

app = Flask('flaskapp')


# ------HOME PAGE------->
@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Renders the home screen.
    """
    return render_template('home.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
    """
    Renders the about screen.
    """
    return render_template('about.html')
# ---------------------->


# <-----LOGIN PAGE-------
@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Checks to see if the session is signed in and if it is, redirects
    to the loginconfirm, and if not renders the login page
    """
    if 'GET':
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return redirect('/loginconfirm')
# --------------------->


# <-----LOGIN CONFIRM PAGE-------
@app.route('/loginconfirm', methods=['GET', 'POST'])
def login_confirm():
    """
    Checks to see if a username exists and then checks if the password
    entered was correct and redirects to the user specific url.
    """
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
    """
    Changes the system status to logged-out and sends the user to the login page.
    """
    session['logged_in'] = False
    return render_template('login.html')
# ----------------------->


# -------New User-------->
@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    """
    Renders the new user creation screen.
    """
    if 'GET':
        return render_template('new_user_creation.html')
# ------------------>


# -----Confirmation Page---->
@app.route('/new_user/confirmation', methods=['GET','POST'])
def confirmation():
    """
    Creates a new user in the dashboard by grabbing all the information
    from the form on the new_user screen. Before creating a new user
    it checks if the user exists, then inserts the info into the database
    and renders a confirmation page.
    """
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
    """
    Renders the reset password screen.
    """
    return render_template('reset_password.html')
# ------------------------------->


# ------Password Reset Confirm----->
@app.route('/reset_password/confirmation', methods=['GET', 'POST'])
def confirm_reset():
    """
    Processes the password reset by checking to see if the phone number
    is the same, then modifies the information in the database and renders
    the confirmation page.
    """
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
    """
    Renders the dashboard for a specific user by first checking if the
    session is logged in.
    """
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        return render_template('dashboard_test.html', username=username, host=HOST, port=PORT)


@app.route('/user/<string:username>/settings', methods=['POST', 'GET'])
def dashboard_settings(username):
    """
    Renders the settings modification page.
    """
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        return render_template('dashboard_settings.html', data=return_user(username))


@app.route('/user/<string:username>/settings/confirmation', methods=['POST', 'GET'])
def dashboard_settings_confirmation(username):
    """
    Updates the settings the user put in.
    """
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


# FRONT DOOR SECTION
# ----------------------------------------------->

# front door sync user to barcode for the night
@app.route('/syncuser', methods=['GET', 'POST'])
def syncuser():
    return render_template('syncuser.html')


@app.route('/confirm', methods=['GET', 'POST'])
def confirm():
    if request.method == 'POST':
        initbarcode = request.form['initbarcode']
        username = request.form['username']
        password = request.form['password']
        success = False  # default is false for syncing success
        # Check if user exists
        if return_user(username) is not None and check_password(username, password):
            sync_user(username, initbarcode)
            success = True
        return render_template('confirm.html', username=username, initbarcode=initbarcode)


# BAR SECTION
# ----------------------------------------------->


@app.route('/barcode', methods=['GET', 'POST'])
def barcode():
    return render_template('barcode.html')


@app.route('/drinkselection', methods=['GET', 'POST'])
def drink_selection():
    if request.method == 'POST':
        barcode = request.form['barcode']
        data = return_data()
        barcodes = [x[6] for x in data]
        success = False
        username = None
        if barcode in barcodes:
            success = True
            index = barcodes.index(barcode)
            username = data[index][2]
        return render_template('drinkbuttons.html', username=username, barcode=barcode, success=success)


# -------Drink Results------>
@app.route('/drinkresults/<string:username>/<string:barcode>', methods=['GET', 'POST'])
def drink(username, barcode):
    if request.method == 'POST':
        mixers = request.form['mixers']
        alcohol = request.form['alcohol']
        print(alcohol)
        print(mixers)
        update_drink(alcohol)
        update_drink(mixers)
        increase_drink_count(barcode)
        write_drink_timestamp(barcode)
        return render_template('drinksresults.html', mixers=mixers, alcohol=alcohol, username=username)


# ------------Party Captain Section---------------------->

# -------New Admin-------->
@app.route('/new_admin', methods=['GET'])
def new_admin():
    """
    Renders the page for new admin creation.
    """
    if 'GET':
        return render_template('newadmin.html')
# ------------------>


# -----Confirmation Page---->
@app.route('/new_admin/confirmation', methods=['GET', 'POST'])
def admin_confirmation():
    """
    Creates a new admin checking to see if the information entered was valid.
    Then renders the admin login page.
    """
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
    """
    Renders the admin login page.
    """
    if 'GET':
        if not session.get('logged_in'):
            return render_template('adminlogin.html')
        else:
            return redirect('/adminloginconfirm')
# --------------------->


# <-----PC LOGIN CONFIRM PAGE-------
@app.route('/adminloginconfirm', methods=['GET', 'POST'])
def admin_login_confirm():
    """
    Checks the entered login information to see if it is correct,
    and if so, renders the admin dashboard for the user routing
    through the admin's url.
    """
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
@app.route('/admin/<string:username>', methods=['POST', 'GET'])  # uses username to send to MultiLinePlot and get the admin settings for max_disp_num
def pc_dashboard(username):
    """
    Renders the party captain (admin) dashboard screen.
    """
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        revenue = get_party_global_data()[0][2]
        expense = get_party_global_data()[0][3]
        profit = revenue - expense
        return render_template('pcdash.html', revenue=revenue, expense=expense, profit=profit, host=HOST, port=PORT, username=username)


@app.route('/admin/<string:username>/new_party', methods=['GET', 'POST'])
def new_party(username):
    """
    This function renders the page for resetting the party
    """
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        return render_template('new_party.html', username=username)


@app.route('/admin/<string:username>/new_party/confirm', methods=['GET', 'POST'])
def new_party_confirm(username):
    """
    This function resets the drinks_times and drinks_data tables
    in the database showing the start of a new party
    """
    if not session.get('logged_in'):
        return redirect('/login')
    else:
        clear_times()
        reset_drink_data()
        reset_party_global_data()
        return redirect('/admin/' + username)


# ---------Plots----------->
@app.route("/multi/<string:username>")
def MultiLinePlot(username):
    """
    Renders the multiline plot of multiple users' BAC.
    """
    party_start = get_party_global_data()[0][0]
    current_time = time.time()
    max_disp_num = return_admin(username)[2]  # returns admin info and selects 3rd entry which is max_disp_num setting
    if max_disp_num > 5:  # more than 5 lines looks too cluttered
        max_disp_num = 5
    res = find_max_BACs(current_time, party_start, max_disp_num)
    values, labels, lines, elements, people_to_disp, colors = res
    return render_template('MultiLinePlot2.html', values=values, labels=labels, lines=lines, elements=elements, people=people_to_disp, colors=colors)


@app.route('/barry', methods=['GET', 'POST'])
def bar_test():
    """
    Renders the bar plot for the amount of drinks in the bar.
    """
    data = sorted([(x[1], x[0]) for x in return_drink_data()])
    labels = [x[1] for x in data]
    values = [x[0] for x in data]
    max_val = values[-1]
    return render_template('BarGraph.html', values=values, labels=labels, max=max_val)


@app.route("/chart/<string:username>")
def chart(username):
    """
    Renders the line plot for a single user's BAC.
    """
    party_start = get_party_global_data()[0][0]
    current_time = time.time()
    res = find_BACS_singleuser(current_time, party_start, username)
    values, labels, lines, elements, person, color, fill_color = res
    return render_template('MultiLinePlot2.html', values=values, labels=labels, lines=lines, elements=elements, people=person, colors=color, fill_color=fill_color)


# -----------End Plots------------------->



if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    # app.run(host=HOST, port=PORT)

    # app.debug = False
    # # app.debug = False
    # toolbar = DebugToolbarExtension(app)

    app.run(host=HOST, port=PORT)     # Use for hosting on localhost
    # HOST = '10.7.68.97'     # use for hosting on single computer on network
    # app.run(host=HOST, port=PORT)
    # app.run('0.0.0.0', '443')
