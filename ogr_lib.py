import sys
import json
import datetime

weekDays = {'monday': 0, 'tuesday': 1, 'wednesday': 2
            , 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
ind_to_day = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}

def day_s(diff):
    if diff == 1:
        return(" day) ")
    else:
        return(" days) ")

class Ogr:
    def __init__(self, data):
        self.dates = data["dates"]
        self.events = data["events"]
        self.weekdays = data["weekdays"]

    def show(self):
        dates = self.dates
        events = self.events
        weekdays = self.weekdays
        for i in range(len(dates)):
            today = datetime.date.today()
            year, month, day = (int(x) for x in dates[i].split('-'))
            _date = datetime.date(year, month, day)
            diff = (_date - today).days
            print("____________________________________")
            print(dates[i], " (", weekdays[dates[i]], " : ", diff, day_s(diff)
                  , "\t[", i, "]", sep='', end=":\n")
            if (len(events[dates[i]]) != 0):
                for j in range(len(events[dates[i]])):
                    print(" -", events[dates[i]][j], " [", j, "]", sep='')


    def open(self, args):
        dates = self.dates
        events = self.events
        weekdays = self.weekdays
        ok = True
        if len(args) < 3:
            print("No arguments");
            ok = False

        date = args[2]
        if date == 'today' or date == 'Today':
            date = datetime.date.today().strftime("%Y-%m-%d")
        elif date == 'tomorrow' or date == 'Tomorrow':
            date = datetime.date.today() + datetime.timedelta(days=1)
            date = date.strftime("%Y-%m-%d")
        elif date[0] == '+':
            shift = int(date[1:])
            date = datetime.date.today() + datetime.timedelta(days=shift)
            date = date.strftime("%Y-%m-%d")
        elif date in weekDays:
            wd = date
            date = datetime.date.today()
            while date.weekday() != weekDays[wd]:
                date += datetime.timedelta(days=1)
            date = date.strftime("%Y-%m-%d")
        elif date == 'next':
            wd = args[3]
            if wd not in weekDays:
                ok = False
            else:
                date = datetime.date.today()
                while date.weekday() != weekDays[wd]:
                    date += datetime.timedelta(days=1)
                date += datetime.timedelta(days=7)
                date = date.strftime("%Y-%m-%d")
        else:
            test = args[2].split('-')
            if len(test) != 3:
                print("Incorrect date format")
                ok = False

        for d in range(len(data["dates"])):
            if data["dates"][d] == date:
                print("Date already exists with index", d)
                ok = False
                break

        if ok:
            data["dates"].append(date)
            data["dates"].sort()
            data["events"][date] = []
            year, month, day = (int(x) for x in date.split('-'))
            _date = datetime.date(year, month, day)
            data["weekdays"][date] = ind_to_day[_date.weekday()]
            self.show()

    def close(self, args):
        dates = self.dates
        events = self.events
        weekdays = self.weekdays
        if int(args[2]) < len(data["dates"]):
            data["events"].pop(data["dates"][int(args[2])])
            data["weekdays"].pop(data["dates"][int(args[2])])
            data["dates"].pop(int(args[2]))
            self.show()
        else:
            print("no such index")

    def add(self, args):
        dates = self.dates
        events = self.events
        weekdays = self.weekdays
        ok = True
        if args[2] != 'to':
            print('Use "add to" instead')
            ok = False
        if ok:
            index = int(args[3])
            text = input()
            data["events"][data["dates"][index]].append(text)
            self.show()

    def rm(self, args):
        ok = True
        if len(args) < 4 or args[3] != "from":
            print('Use "rm <index> from <index>" instead')
            ok = False
        if ok and len(data["dates"]) <= int(args[4]):
            print("index out of range")
            ok = False
        if ok and len(data["events"][data["dates"][int(args[4])]]) <= int(args[2]):
            print("index out of range")
            ok = False
        if ok:
            data["events"][data["dates"][int(args[4])]].pop(int(args[2]))
            self.show()

    def clear(argv):
        if int(args[2]) < len(data["dates"]):
            data["events"][data["dates"][int(args[2])]] = []
            show(data)
        else:
            print("no such index")

    def help(self):
        print("No such command")
        print("Possible commands:\n")

        print("[<empty>]")

        print("[open <date>]")
        print("[open today]")
        print("[open tomorrow]")
        print("[open <day of the week>]")
        print("[open next <day of the week>]")
        print("[open +<number of days>]")

        print("[close <index>]")
        print("[clear <index>]")
        print("[add to <index>]")
        print("[rm <index> from <index>]")
