from BAC import *
from database_test import *
from datetime import datetime as dt


def find_BACS_singleuser(current_time, party_start, username):
    labels = []
    user = return_user(username)
    person = [username]
    barcode = user[6]
    drink_times = get_drink_timestamp(barcode)
    drink_times = [x for x in drink_times if x is not None]
    height = user[7]
    weight = user[8]*453.592
    gender = user[10][0]
    res = BAC(height, weight, gender, drink_times, current_time, party_start)
    minute_labels = res[0]
    for time in minute_labels:  # converting minute float labels to time strings
        seconds = time*60 + party_start
        dt_obj = dt.fromtimestamp(seconds)
        labels.append(dt_obj.strftime("%I:%M%p"))
    values = res[1]
    lines = 1
    elements = len(values)
    color = ["rgba(169,68,66,1)"]
    return [values, labels, lines, elements, person, color]
