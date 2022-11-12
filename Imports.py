import threading
class Eventday:
    def __init__(self, datee, starttime, endtime):
        self.date = datee
        self.starttime = starttime
        self.endtime = endtime

    def updateEndTime(self, newendtime):
        if newendtime > self.endtime:
            self.endtime = newendtime

    def updateStartTime(self, newstarttime):
        #print("nst", newstarttime)
        #print("st", self.starttime)
        if newstarttime < self.starttime:
            self.starttime = newstarttime

class EventList:
    def __init__(self):
        self.listOfEvents = []

    def handle(self, datee, starttime, endtime):
        #print(date, starttime, endtime)
        binResult = binarySearch(self.listOfEvents, datee)
        if (binResult != -1):
            self.listOfEvents[binResult].updateStartTime(starttime)
            self.listOfEvents[binResult].updateEndTime(endtime)

        else:
            self.listOfEvents.append(Eventday(datee, starttime, endtime))
                    #print("Nicht vorhanden")

def handleURL(inputurl):
    cal_i = requests.get(inputurl).text
    split_overhead = cal_i.split("END:VTIMEZONE")
    split_events = split_overhead[1].split("BEGIN:VEVENT")
    return split_events

class myThread(threading.Thread):
    def __init__(self, url):
        threading.Thread.__init__(self)
        self.url = url
        self.value = None

    def run(self):
        self.value = handleURL(self.url)


def handleEvents(eventlist):
    eventlistobject = EventList()
    for event in eventlist:
        date = 0
        endt = 0
        stime = 0
        remote = False
        for line in event.splitlines():
            if "DTEND" in line:
                date = line.split(":")[1].split("T")[0]
                endt = line.split(":")[1].split("T")[1]
                # print(date)
            if "DTSTART" in line:
                stime = line.split(":")[1].split("T")[1]
            if "Raum Online" in line:
                remote = True
            #print(date, endt, stime)
        if not remote and stime !=0:
                eventlistobject.handle(date, stime, endt)
    return eventlistobject


def binarySearch(list, value):
    low = 0
    high = len(list) - 1
    middle = 0

    while low <= high:
        middle = (high + low) //2
        if list[middle].date < value:
            low = middle +1
        elif list[middle].date > value:
            high = middle -1
        else:
            return middle
    return -1