import urllib
import json


def clean_data(f):
    data = []
    for line in f:

        tmp = {
            "username": line[0:9].strip(),
            "access type": line[9:22].strip(),
            "ip": line[22:39].strip(),
            "date": line[39:49].strip(),
            "time interval": line[49:].strip(),
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
    ""


def get_ip_data(data):
    ip = get_ips_as_list(data)
    countries = []

    for i in ip:
        countries.append(do_req(i))

    return countries


def create_pie(data):
    print("")


def main():

    f = open("logins.txt", "r")
    data = clean_data(f)
    create_pie(get_ip_data(data))


main()
