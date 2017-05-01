from BAC import *
from database_test import *


def find_max_BACs(current_time, party_start, max_disp_num):
    people = []
    people_to_disp = []
    final_bacs = []
    bac_series = []
    values = []
    labels = []
    data = return_data()
    first_run = True
    for user in data:
        person = user[2]
        people.append(person)
        barcode = user[6]
        drink_times = get_drink_timestamp(barcode)
        drink_times = [x for x in drink_times if x is not None]
        height = user[7]
        weight = user[8]
        gender = user[10][0]
        res = BAC(height, weight, gender, drink_times, current_time, party_start)
        if first_run:
            labels = res[0]
            first_run = False
        bac_series.append(res[1])
        final_bacs.append(res[1][-1])
    final_bacs_sorted = sorted([(value, index) for index, value in enumerate(final_bacs)], reverse=True)
    for i in range(max_disp_num):
        index = final_bacs_sorted[i][1]
        people_to_disp.append(people[index])
        this_bac_series = bac_series[index]
        for val in this_bac_series:
            values.append(val)
    lines = max_disp_num
    elements = len(values)
    colors = ["rgba(169,68,66,1)", "rgba(60,118,61,1)", "rgba(49,112,143,1)"]
    colors = colors[0:lines]
    return [values, labels, lines, elements, people_to_disp, colors]
