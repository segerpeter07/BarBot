"""
Party captain dashboard
"""

import os
from flask import Flask, render_template, request
from database_test import *

app = Flask('flaskapp')


@app.route('/pcdash', methods=['GET', 'POST'])
def pcdashboard():
    revenue = 100
    expense = 50
    profit = revenue - expense
    return render_template('pcdash.html', revenue=revenue, expense=expense, profit=profit, host=HOST, port=PORT)


@app.route("/liney")
def LinePlot():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('LinePlotTemplate.html', values=values, labels=labels)


@app.route("/multi")
def MultiLinePlot():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [[10, 9, 8, 7, 6, 4, 7, 8], [1, 2, 3, 7, 5, 3, 9, 10], [3, 6, 7, 4, 5, 3, 2, 7]]
    lines = len(values)
    values = [10, 9, 8, 7, 6, 4, 7, 8, 1, 2, 3, 7, 5, 3, 9, 10, 3, 6, 7, 4, 5, 3, 2, 7]
    lines = 3
    elements = len(values)
    return render_template('MultiLinePlot.html', values=values, labels=labels, lines=lines, elements=elements)


@app.route('/barry', methods=['GET', 'POST'])
def bar_test():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('BarGraph.html', values=values, labels=labels)


if __name__ == '__main__':
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
