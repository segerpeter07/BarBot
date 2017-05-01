from BAC import *
from database_test import *
from datetime import datetime as dt


def find_max_BACs(current_time, party_start, max_disp_num):
    people = []  # empty list to contain all users' usernames
    people_to_disp = []  # empty list to contain usernames of n people with highest bacs, n = max_disp_num
    final_bacs = []  # empty list to store final bacs of each user in order to sort and select out highest bacs
    bac_series = []  # empty list to store all bac series, once final_bacs is sorted these series will be selected out and appended to values
    values = []  # empty list to contain final list of values of bacs for highest users
    labels = []  # empty list to contain time strings of time series for plotting
    data = return_data()  # returns all account_holder data as a list of tuples
    if max_disp_num > len(data):  # make sure max_disp_num cannot exceed number of people (records) in database
        max_disp_num = len(data)
    first_run = True  # this is used to only pull the time series once since it is the same for all users
    for user in data:  # iterate through each user's information tuple
        person = user[2]  # username is 3rd entry in tuple
        people.append(person)
        barcode = user[6]  # barcode is 7th entry in tuple
        drink_times = get_drink_timestamp(barcode)  # uses database_test function to return list of times in seconds from epoch at which user took a drink
        drink_times = [x for x in drink_times if x is not None]  # removes null values from list, some users may have taken more drinks than others
        height = user[7]  # height is 8th entry in tuple
        weight = user[8]  # weight is 9th entry in tuple
        gender = user[10][0]  # gender is 11th entry in tuple, only the first letter is needed to determine gender in BAC.py
        res = BAC(height, weight, gender, drink_times, current_time, party_start)  # runs BAC.py func, returns list of two lists [time series, bac series]
        if first_run:  # just sets the time series the first time this for loop runs, this time series is then converted to time strings
            minute_labels = res[0]
            first_run = False
        bac_series.append(res[1])
        final_bacs.append(res[1][-1])  # appends final value of bac_series for each user, this will create a list of current bacs for each user
    # final_bacs_sorted creates list of tuples containing value and index sorted by final_bacs
    final_bacs_sorted = sorted([(value, index) for index, value in enumerate(final_bacs)], reverse=True)
    for i in range(max_disp_num):  # appends people and bac_series to people_to_disp and values respectively for number (max_disp_num) of users with high bacs
        index = final_bacs_sorted[i][1]  # finds index of highest values (second number in tuple is index)
        people_to_disp.append(people[index])
        this_bac_series = bac_series[index]
        # appends each value as opposed to appending list, this is due to JS workaround because we weren't able to convert python list of lists into a list of
        # lists in JS using jinja
        for val in this_bac_series:
            values.append(val)
    lines = max_disp_num  # lines is number of series to plot
    elements = len(values)  # elements is number of data points in series, needed for plotting in JS
    colors = ["rgba(169,68,66,1)", "rgba(60,118,61,1)", "rgba(49,112,143,1)", "rgba(230,138,0,1)", "rgba(153,0,153,1)"]  # colors are for different line colors
    colors = colors[0:lines]  # selects number of colors equal to lines on plot
    for time in minute_labels:  # converting minute float labels to time strings
        seconds = time*60 + party_start
        dt_obj = dt.fromtimestamp(seconds)
        labels.append(dt_obj.strftime("%I:%M%p"))
    return [values, labels, lines, elements, people_to_disp, colors]
