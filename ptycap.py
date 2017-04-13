"""
Party captain dashboard
"""

import os
from flask import Flask, render_template, request

app = Flask('flaskapp')


@app.route('/pcdash', methods=['GET', 'POST'])
def pcdashboard():
    return render_template('pcdash.html')


@app.route("/chart")
def chart():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('LinePlotTemplate.html', values=values, labels=labels)


@app.route('/plotty', methods=['GET', 'POST'])
def plot_test():
    return render_template('LinePlotTemplate.html')


@app.route('/barry', methods=['GET', 'POST'])
def bar_test():
    return render_template('BarGraph.html')


if __name__ == '__main__':
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)