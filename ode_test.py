import matplotlib.pyplot as plt
import numpy as np

height = 70  # inches, might be used to map a lbm percentage based on bmi
weight = 180*453.592  # grams
gender = 'M'  # 'M' for male, 'F' for female
drink_times = [1, 10, 30, 60, 120, 180]  # list of drink times in minutes
drink_size = 28.3495  # standard drink size in grams
Vm_male = 0.470/10/60  # g/dL-min
Vm_female = 0.480/10/60  # g/dL-min
Km_male = 0.380/10  # g/dL
Km_female = 0.405/10  # g/dL
lbm_density = 1.1*100  # overall density of lean body mass in g/dL or g/cm3
lbm_per_male = .79  # average lean body mass percentage for males, range 76-82
lbm_per_female = .72  # average lean body mass percentage for females, range 69-75


def rate(bac, t):
    if int(t) in drink_times:
        if gender == 'M':
            intake = drink_size/(weight*lbm_per_male/lbm_density)
        else:
            intake = drink_size/(weight*lbm_per_female/lbm_density)
    else:
        intake = 0

    if gender == 'M':
        out = (Vm_male * bac)/(bac + Km_male)
    else:
        out = (Vm_female * bac)/(bac + Km_female)

    dydt = intake - out
    return dydt


t = np.linspace(1, 1200, 1200)
bac0 = 0


def my_euler(rate, y0, t):
    y = y0
    ys = []
    last_time = 0
    for time in t:
        dt = time - last_time
        dydt = rate(y, time)
        y = dydt * dt + y
        ys.append(y)
        last_time = time
    return ys


bac = my_euler(rate, bac0, t)
plt.plot(t, bac)
plt.show()
