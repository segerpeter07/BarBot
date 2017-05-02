"""
Party captain dashboard
"""

import os
from flask import Flask, render_template, request
from find_max_BACs import *
from database_test import *
import time

app = Flask('flaskapp')


@app.route('/pcdash/<string:username>')  # uses username to send to MultiLinePlot and get the admin settings for max_disp_num
def pcdashboard(username):
    revenue = 100
    expense = 50
    profit = revenue - expense
    return render_template('pcdash.html', revenue=revenue, expense=expense, profit=profit, host=HOST, port=PORT, username=username)


@app.route("/liney")
def LinePlot():
    labels = ["January", "February", "March", "April", "May", "June", "July", "August"]
    values = [10, 9, 8, 7, 6, 4, 7, 8]
    return render_template('LinePlotTemplate.html', values=values, labels=labels)


@app.route("/multi/<string:username>")
def MultiLinePlot(username):
    party_start = get_party_start()
    current_time = 1493026634.7893  # change to time.time() when actuallly running
    max_disp_num = return_admin(username)[2]  # returns admin info and selects 3rd entry which is max_disp_num setting
    if max_disp_num > 5:  # more than 5 lines looks too cluttered
        max_disp_num = 5
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
