"""
Party captain dashboard
"""

import os
from flask import Flask, render_template, request
from find_max_BACs import *

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
    party_start = 1493008634.6537
    current_time = 1493026634.7893
    max_disp_num = 2  # maximum number of users to display on graph
    if max_disp_num > 3:  # temporary hack because there are only 3 colors in the colors list
        max_disp_num = 3
    res = find_max_BACs(current_time, party_start, max_disp_num)
    values, labels, lines, elements, people_to_disp, colors = res
    return render_template('MultiLinePlot2.html', values=values, labels=labels, lines=lines, elements=elements, people=people_to_disp, colors=colors)


@app.route('/barry', methods=['GET', 'POST'])
def bar_test():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('BarGraph.html', values=values, labels=labels)


if __name__ == '__main__':
    HOST = '0.0.0.0' if 'PORT' in os.environ else '127.0.0.1'
    PORT = int(os.environ.get('PORT', 5000))
    app.run(host=HOST, port=PORT)
