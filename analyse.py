import matplotlib.pyplot as plt
from datetime import datetime
import datetime as dt
import time
import classic_metod as cm
import modified_method as mm
import method as mmm


def draw_one_graph(_time, title):
    n = len(_time)
    x = []
    for i in range(1, n + 1, 1):
        x.append(i)
    plt.plot(x, _time)
    plt.title(title)
    plt.ylabel('time')
    plt.show()


def draw_compare(time1, time2, title):
    if len(time1) != len(time2):
        return ValueError
    n = len(time1)
    x = []
    for i in range(1, n + 1, 1):
        x.append(i)
    average_classic_time = calculate_average_time(time1)
    average_modified_time = calculate_average_time(time2)
    plt.plot(x, time1, label="Classic method, average time = " + str(average_classic_time))
    plt.plot(x, time2, label="Modified method, average time = " + str(average_modified_time))
    plt.title(title)
    plt.ylabel('time')
    plt.legend(bbox_to_anchor=(0, -0.15, 1, 0), loc=1, mode="expand", borderaxespad=0)
    plt.show()


def draw_many(_time, title):
    n = len(_time[0])
    x = []
    for i in range(1, n + 1, 1):
        x.append(i)
    average_modified_time_1 = calculate_average_time(_time[0])
    average_modified_time_2 = calculate_average_time(_time[1])
    average_modified_time_3 = calculate_average_time(_time[2])
    average_modified_time_4 = calculate_average_time(_time[3])
    average_modified_time_5 = calculate_average_time(_time[4])
    plt.plot(x, _time[0], label="128 bits, average time = " + str(average_modified_time_1))
    plt.plot(x, _time[1], label="256 bits, average time = " + str(average_modified_time_2))
    plt.plot(x, _time[2], label="512 bits, average time = " + str(average_modified_time_3))
    plt.plot(x, _time[3], label="1024 bits, average time = " + str(average_modified_time_4))
    plt.plot(x, _time[4], label="2048 bits, average time = " + str(average_modified_time_5))
    plt.title(title)
    plt.ylabel('time')
    plt.legend(bbox_to_anchor=(0, -0.15, 1, 0), loc=1, mode="expand", borderaxespad=0)
    plt.show()


def draw_by_points(_time, bits):
    plt.title("Dependence of average time on the key's size")
    plt.plot(bits, _time, 'o')
    plt.plot(bits, _time)
    plt.ylabel('time')
    plt.xlabel('number of bits')
    plt.show()


def calculate_average_time(_time):
    n = len(_time)
    s = 0.0
    for t in _time:
        s += t
    return round(s / n, 3)


def time_classic(messages, nbits):
    times = []
    for m in messages:
        start_time = datetime.now()
        public, private = cm.gen_keys(nbits)
        crypto = cm.encrypt(m, public)
        enc_message = cm.decrypt(crypto, private)
        times.append((datetime.now() - start_time).total_seconds())
    return times


def time_modified(messages, nbits):
    times = []
    for m in messages:
        start_time = datetime.now()
        public, private = mm.gen_keys(nbits)
        crypto = mm.encrypt(m, public)
        enc_message = mm.decrypt(crypto, private)
        times.append((datetime.now() - start_time).total_seconds())
    return times


def time_simple(messages, nbits):
    times = []
    for m in messages:
        start_time = datetime.now()
        public, private = mmm.gen_keys(nbits)
        crypto = mmm.encrypt(m, public)
        enc_message = mmm.decrypt(crypto, private)
        times.append((datetime.now() - start_time).total_seconds())
    return times
