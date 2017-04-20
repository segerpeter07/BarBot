"""
Put your Flask app code here.
"""
import os
from flask import Flask, render_template, request, url_for, redirect
from jinja2 import Environment, FileSystemLoader
from database_test import update_info, return_user, increase_drink_count
import time
import datetime
# create the application object

app = Flask(__name__)
tpldir = os.path.dirname(os.path.abspath(__file__))+'/templates/'
env = Environment(loader=FileSystemLoader(tpldir), trim_blocks=True)


@app.route('/', methods=("GET", "POST"))
def home():
    username = request.form.get('firstname')
    if request.method == 'POST':
        return redirect(url_for('dashboard', firstname=username))
    return render_template('NateLoginTest.html')


@app.route('/<string:firstname>', methods=['GET', 'POST'])
def dashboard(firstname=None):
    firstname = return_user(firstname)
    firstname = firstname[2]
    return render_template('dashboard_test.html', firstname=firstname)


@app.route("/chart")
def chart():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    recent_drink = increase_drink_count('hello')
    labels = ['vodka', 'rum', 'whiskey']
    values = [recent_drink, recent_drink, recent_drink]
    return render_template('LinePlotTemplate.html', values=values, labels=labels)


@app.route("/settings")
def settings(firstname=None):
    firstname = 'natedoggy'
    if request.method == 'POST':
        return redirect(url_for('dashboard', firstname=firstname))
    return render_template('DashBoard_Settings.html')


# start the server with the 'run()' method
if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
