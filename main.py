import sys

import requests
from concurrent import futures


class Eventday:
    def __init__(self, date, start_time, end_time):
        self.date = date
        self.start_time = start_time
        self.end_time = end_time

    def update_end_time(self, new_end_time):
        if new_end_time > self.end_time:
            self.end_time = new_end_time

    def update_start_time(self, new_start_time):
        if new_start_time < self.start_time:
            self.start_time = new_start_time


def day_handler(date, start_time, end_time, list):
    binary_result = binary_search(list, date)
    if binary_result != -1:
        list[binary_result].update_start_time(start_time)
        list[binary_result].update_end_time(end_time)

    else:
        list.append(Eventday(date, start_time, end_time))


def url_handler(url):
    cal_i = requests.get(url).text
    split_overhead = cal_i.split("END:VTIMEZONE")
    return split_overhead


def event_handler(split_cal_file):
    split_events = split_cal_file[1].split("BEGIN:VEVENT")
    events = []
    for event in split_events:
        date = None
        end_time = None
        start_time = None
        remote = False
        for line in event.splitlines():
            if "DTEND" in line:
                date = line.split(":")[1].split("T")[0]
                end_time = line.split(":")[1].split("T")[1]
            if "DTSTART" in line:
                start_time = line.split(":")[1].split("T")[1]
            if "Raum Online" in line:
                remote = True
        if not remote and start_time is not None:
            day_handler(date, start_time, end_time, events)
    return events


def binary_search(list, value):
    low = 0
    high = len(list) - 1

    while low <= high:
        middle = (high + low) // 2
        if list[middle].date < value:
            low = middle + 1
        elif list[middle].date > value:
            high = middle - 1
        else:
            return middle
    return -1


url1 = input("Input URL No.1:")
url2 = input("Input URL No.2:")
with futures.ThreadPoolExecutor(max_workers=2) as pool:
    future1 = pool.submit(url_handler, url1)
    future2 = pool.submit(url_handler, url2)
try:
    split_cal_file_1 = future1.result()
    split_cal_file_2 = future2.result()
except requests.RequestException as exception:
    print("Error while handling URL!")
    print("Exception:", str(exception))
    sys.exit(1)

if (len(split_cal_file_1) == 1):
    print("WARNING: The given URL1 is not a supported .ical file.")
    print("Script stopped")
    sys.exit(1)
elif (len(split_cal_file_2) == 1):
    print("WARNING: The given URL2 is not a supported .ical file.")
    print("Script stopped")
    sys.exit(1)

eventlist_1 = event_handler(split_cal_file_1)
eventlist_2 = event_handler(split_cal_file_2)

if (len(eventlist_1) == 1):
    print("WARNING: The given URL1 is an empty calendar.")
    print("Script stopped")
    sys.exit(1)
elif (len(eventlist_2) == 1):
    print("WARNING: The given URL2 is an empty calendar.")
    print("Script stopped")
    sys.exit(1)

for day in eventlist_1:
    for day2 in eventlist_2:
        if day.date == day2.date:
            if day.start_time == day2.start_time and day.end_time == day2.end_time:
                print("Match: " + day.date)
