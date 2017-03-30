"""
Put your Flask app code here.
"""
import os
from flask import Flask, render_template, request, url_for, redirect, session
from jinja2 import Environment, FileSystemLoader
# create the application object

app = Flask(__name__)
tpldir = os.path.dirname(os.path.abspath(__file__))+'/templates/'
env = Environment(loader=FileSystemLoader(tpldir), trim_blocks=True)


@app.route('/', methods = ("GET", "POST"))
def home():
    username = request.form.get('username')
    if request.method == 'POST':
        return redirect(url_for('dashboard', firstname=username))
    return render_template('NateLoginTest.html')


@app.route('/<string:firstname>', methods=['GET', 'POST'])
def dashboard(firstname=None):
    return render_template('dashboard_test.html', firstname=firstname)


@app.route("/chart")
def chart():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('LinePlotTemplate.html', values=values, labels=labels)


# start the server with the 'run()' method
if __name__ == '__main__':
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
