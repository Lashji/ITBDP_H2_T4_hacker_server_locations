import urllib.request
import json
import time
import matplotlib.pyplot as plt
import numpy as np
import math


def clean_data(f):
    data = []
    for line in f:

        tmp = {
            "username": line[0:9].strip(),
            "access type": line[9:22].strip(),
            "ip": line[22:39].strip(),
            "date": line[39:49].strip(),
            "time": line[49:].strip(),
        }

        if tmp["date"] == "Tue Oct  2":
            data.append(tmp)
    return data


def get_ips_as_list(data):
    tmp = []
    for d in data:
        if d["ip"] not in tmp:
            tmp.append(d["ip"])
    return tmp


def do_req(ip):
    req = urllib.request.urlopen("https://www.iplocate.io/api/lookup/"+ip)
    data = json.loads(req.read())
    return data


def get_country_index(data, country):
    for i in range(len(data)):
        if data[i]["country"] == country:
            return i
    return -1


def obj_in_countries(countries, country_name):
    for c in countries:
        if c["country"] == country_name:
            return True
    return False


def get_top_ten_countries(countries):
    tmp = []

    maxc = countries[0]
    clist = countries

    for i in range(10):
        maxc = clist[0]

        for c in clist:
            num = c["count"]
            if num > maxc["count"]:
                maxc = c
        tmp.append(maxc)
        clist[:] = [i for i in clist if i["country"] != maxc["country"]]

    return tmp


def get_ip_data(data):
    ip = get_ips_as_list(data)
    countries = []

    for i in ip:
        data = do_req(i)

        if data["country"]:

            obj = {
                "country": data["country"],
                "count": 1
            }

            if not obj_in_countries(countries, obj["country"]):
                countries.append(obj)
            else:
                countries[get_country_index(
                    countries, data["country"])]["count"] += 1

        time.sleep(1)
    return countries


def create_pie(data):

    if len(data) > 10:
        data = get_top_ten_countries(data)

    labels = []
    counts = []
    for i in data:
        labels.append(i["country"])
        counts.append(i["count"])
    fig1, ax1 = plt.subplots()
    ax1.pie(counts, labels=labels, autopct='%1.1f%%')
    ax1.axis('equal')
    save_chart(fig1, "hackpie.png")
    # plt.show()


def clean_data_time_string(s):
    return s[:2]


def get_attack_start_times(data):
    tmp = []
    for d in data:
        tmp.append(int(clean_data_time_string(d["time"])))
    return tmp


def create_time_chart(data):
    times = get_attack_start_times(data)

    ar = np.arange(0, 24, 1)
    tmp = list(range(0, 24))

    for i in times:
        tmp[i] += 1

    fig = plt.figure()
    width = 0.7

    ax = fig.gca()
    ax.bar(ar, tmp,  width)
    ax.set_xlabel("Time")
    ax.set_ylabel("Attacks")
    ax.set_title("Attacks on Weto server Tue Oct 2")
    ax.set_xticks(ar)
    ax.set_xticklabels(ar)
    save_chart(fig, "hackbar.png")
    # plt.show()


def save_chart(fig, filename):
    fig.savefig(filename, bbox_inches='tight')


def main():

    f = open("logins.txt", "r")
    data = clean_data(f)
    create_pie(get_ip_data(data))
    create_time_chart(data)


main()
