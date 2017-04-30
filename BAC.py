import numpy as np

# height = 70  # inches, might be used to map a lbm percentage based on bmi
# weight = 180*453.592  # grams
# gender = 'M'  # 'M' for male, 'F' for female
# drink_times = [1, 10, 30, 60, 120, 180]  # list of drink times in minutes
drink_size = 28.3495*1.5*0.4  # standard drink size in grams
Vm_male = 0.470/10/60  # g/dL-min
Vm_female = 0.480/10/60  # g/dL-min
Km_male = 0.380/10  # g/dL
Km_female = 0.405/10  # g/dL
lbm_density = 1.1*100  # overall density of lean body mass in g/dL or g/cm3
lbm_per_male = .79  # average lean body mass percentage for males, range 76-82
lbm_per_female = .72  # average lean body mass percentage for females, range 69-75


def rate(bac, t, height, weight, gender, drink_times):
    if gender == 'M':
        Vm = Vm_male
        Km = Km_male
        lbm_per = lbm_per_male
    else:
        Vm = Vm_female
        Km = Km_female
        lbm_per = lbm_per_female

    if int(t) in drink_times:
        intake = drink_size/(weight*lbm_per/lbm_density)
    else:
        intake = 0

    out = (Vm * bac)/(bac + Km)

    dydt = intake - out
    return dydt


def my_euler(rate, y0, t, height, weight, gender, drink_times):
    y = y0
    ys = []
    last_time = 0
    for time in t:
        dt = time - last_time
        dydt = rate(y, time, height, weight, gender, drink_times)
        y = dydt * dt + y
        ys.append(y)
        last_time = time
    return ys


def sec_to_min(time_sec):
    return int(time_sec/60)


def BAC(height, weight, gender, drink_times, current_time, party_start, bac0=0):
    drink_times = [sec_to_min(time - party_start) for time in drink_times]
    end_time = sec_to_min(current_time - party_start)
    t = np.linspace(1, end_time, end_time)
    bac = my_euler(rate, bac0, t, height, weight, gender, drink_times)
    return [t, bac]
