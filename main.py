import requests
import Imports
import threading

url1 = input("Input URL No.1:")
url2 = input("Input URL No.2:")
t1 = Imports.myThread(url1)
t2 = Imports.myThread(url2)
t1.start()
t2.start()
t1.join()
t2.join()
split_events1 = t1.value
split_events2 = t2.value
EventListObject = Imports.handleEvents(split_events1)
EventListObject2 = Imports.handleEvents(split_events2)

for day in EventListObject.listOfEvents:
    for day2 in EventListObject2.listOfEvents:
        if day.date == day2.date:
            if day.starttime == day2.starttime and day.endtime == day2.endtime:
                print("Match: " + day.date)