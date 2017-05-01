"""
Party captain dashboard
"""

import os
from flask import Flask, render_template, request
from database_test import *
from BAC import *

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
    res1 = BAC(70, 180*453.592, 'M', [60, 600, 1800, 3600, 7200, 10800], 18000, 0)
    res2 = BAC(68, 200*453.592, 'F', [1800, 5400, 7200, 14400], 18000, 0)
    res3 = BAC(62, 120*453.592, 'F', [900, 3600, 5400, 7200, 10800, 14400], 18000, 0)
    labels = res1[0]
    lines = 3
    values = res1[1]
    for item in res2[1]:
        values.append(item)
    for item in res3[1]:
        values.append(item)
    elements = len(values)
    people = ['Lucky', 'Kian', 'Peter']
    colors = ["rgba(169,68,66,1)", "rgba(60,118,61,1)", "rgba(49,112,143,1)"]
    return render_template('MultiLinePlot2.html', values=values, labels=labels, lines=lines, elements=elements, people=people, colors=colors)


@app.route('/barry', methods=['GET', 'POST'])
def bar_test():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('BarGraph.html', values=values, labels=labels)


if __name__ == '__main__':
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
