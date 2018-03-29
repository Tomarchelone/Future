import sys
import json
import datetime

weekDays = {'monday': 0, 'tuesday': 1, 'wednesday': 2
            , 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6,
            'Monday': 0, 'Tuesday': 1, 'Wednesday': 2
            , 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
ind_to_day = {0: 'Mon', 1: 'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat'
              , 6: 'Sun'}
ind_to_month = {1: 'Yanuary', 2: 'February', 3: 'March', 4: 'April', 5: 'May'
                , 6: 'June', 7: "July", 8: "August", 9: "September"
                , 10: "October", 11: "November", 12: "December"}


def day_s(diff):
    if diff == 1:
        return("day")
    else:
        return("days")

class Ogr:
    def __init__(self, data):
        self.window = data["window"]
        self.dates = data["dates"]
        self.events = data["events"]
        self.weekdays = data["weekdays"]
        self.cycles = list(map(lambda x: Cycle(x), data["cycles"]))

    def show(self):
        dates = self.dates
        events = self.events
        weekdays = self.weekdays
        window = self.window
        today = datetime.date.today()

        print("<<<< Events for the next ", window, " ", day_s(window), " >>>>", sep='')

        index = -1
        for i in range(window):
            date = today + datetime.timedelta(days=i)
            flat_date = flatten(date)

            taken = False

            if flat_date in self.events:
                index += 1
                print("____________________________________")
                print(flat_date, " (", weekdays[flat_date], " : ", i, " ", day_s(i)
                      , ")\t[", index, "]", sep='', end=":\n")
                taken = True
                if (len(events[flat_date]) != 0):
                    for j in range(len(events[flat_date])):
                        print(" -", events[flat_date][j], " [", j, "]", sep='')

            for c_index in range(len(self.cycles)):
                cycle = self.cycles[c_index]
                if (cycle.falls(date)):
                    if not taken:
                        print("____________________________________")
                        print(flat_date, " (", ind_to_day[date.weekday()], " : "
                        , i, " ", day_s(i), ")\t[C]", sep='', end=":\n")
                    print(" -", cycle.text, _type(cycle), "[", c_index, "]", sep='')


    def open(self, args):
        dates = self.dates
        events = self.events
        weekdays = self.weekdays
        if len(args) < 3:
            print("No arguments");
            return()

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
                return()
            else:
                date = datetime.date.today()
                while date.weekday() != weekDays[wd]:
                    date += datetime.timedelta(days=1)
                date += datetime.timedelta(days=7)
                date = date.strftime("%Y-%m-%d")
        else:
            test = list(args[2].split('-'))
            if len(test) != 3 or len(test[0]) != 4:
                print("Incorrect date format\nUse yyyy-mm-dd format")
                return()


        for d in range(len(dates)):
            if dates[d] == date:
                print("Date already exists with index", d)
                return()

        dates.append(date)
        dates.sort()
        events[date] = []
        year, month, day = (int(x) for x in date.split('-'))
        _date = datetime.date(year, month, day)
        weekdays[date] = ind_to_day[_date.weekday()]
        self.show()

    def close(self, args):
        dates = self.dates
        events = self.events
        weekdays = self.weekdays
        if int(args[2]) < len(dates):
            events.pop(dates[int(args[2])])
            weekdays.pop(dates[int(args[2])])
            dates.pop(int(args[2]))
            self.show()
        else:
            print("no such index")

    def add(self, args):
        dates = self.dates
        events = self.events
        weekdays = self.weekdays
        if args[2] != 'to':
            print('Use "add to" instead')
            return()
        index = int(args[3])
        text = input()
        events[dates[index]].append(text)
        self.show()

    def rm(self, args):
        if len(args) < 4 or args[3] != "from":
            print('Use "rm <index> from <index>" instead.')
            return()
        if len(self.dates) <= int(args[4]):
            print("index out of range")
            return()
        if len(self.events[self.dates[int(args[4])]]) <= int(args[2]):
            print("index out of range")
            return()

        self.events[self.dates[int(args[4])]].pop(int(args[2]))
        self.show()

    def clear(self, args):
        if int(args[2]) < len(self.dates):
            self.events[self.dates[int(args[2])]] = []
            self.show()
        else:
            print("no such index")

    def cycle(self, args):
        if args[2] == "year":
            mm, dd = (int(x) for x in args[3].split('-'))
            self.cycles.append(Cycle([0, mm, dd, -1, -1, input()]))
        elif args[2] == "month":
            dd = int(args[3])
            self.cycles.append(Cycle([1, dd, -1, -1, -1, input()]))
        elif args[2] == "week":
            self.cycles.append(Cycle([2, args[3], -1, -1, -1, input()]))
        elif args[2] == "every":
            if (args[3] != "days," or args[4] != "start"):
                print("Use 'cycle every <number of days> days, start <yyyy-mm-dd>' instead.")
                return()

            diff = int(args[3])
            yy, mm, dd = (int(x) for x in args[7].split('-'))
            self.cycles.append(Cycle([3, yy, mm, dd, diff, input()]))

        # self.show()

    def stop_cycle(self, args):
        self.cycles.pop(int(args[2]))

    def show_cycles(self, args):
        if args[2] != "cycles":
            print("Use 'show cycles' instead.")
            return()

        for i in range(len(self.cycles)):
            print(i, ": ", self.cycles[i].text
            , sep='', end='')

            if (self.cycles[i].type == 0):
                print(", ", ind_to_month[self.cycles[i].field1], " "
                , self.cycles[i].field2, sep='')

            elif (self.cycles[i].type == 1):
                print(", ", self.cycles[i].field1, ending(self.cycles[i].field1)
                , " of each month", sep='')
            elif (self.cycles[i].type == 2):
                print(", ", self.cycles[i].field1
                , " of each week", sep='')
            else:
                print(", every",  self.cycles[i].field4
                , " days", sep='')

    def show_window(self):
        print("Window size is", self.window, "days")

    def set_window(self, args):
        if (args[2] == 'window'):
            self.window = int(input())
        else:
            print('No such command. To set window use "set window"')

    def data(self):
        data = {}

        data["dates"] = self.dates
        data["events"] = self.events
        data["weekdays"] = self.weekdays
        data["cycles"] = sorted(list(map(lambda x: x.recycle(), self.cycles)), key=get_last)
        data["window"] = self.window
        return(data)


    def help(self):
        print("Possible commands:\n")
        print("All commands should start with 'ogr'\n")

        print("-[] : empty command (typed as 'ogr') - view list of events \n")

        print("-[open <yyyy-mm-dd>] : open date for listing")
        print("-[open today]")
        print("-[open tomorrow]")
        print("-[open <day of the week>]")
        print("-[open next <day of the week>]")
        print("-[open +<number of days>] : open +1 means  open tomorrow\n")

        print("All dates have indexes in their right corner\n")

        print("-[close <index>] : close date with index <index>;"
        , "it will disappear from list")
        print("-[clear <index>] : clear all events from date")
        print("-[add to <index>] : add an event to date\n")

        print("Every event has it's own index at the end of them\n")

        print("-[rm <index> from <index>] rm event from date\n")

        print("There is a variable 'window' that represents maximun distance"
        , "that listed dates can have from today. Other dates will not be"
        , "shown until they are close enough\n")

        print("-[set window] : sets window size\n")

        print("There is a special command for cyclic events\n")

        print("-[cycle year <mm-dd>] : annual cycle")
        print("-[cycle month <day of the month>] : montly cycle")
        print("-[cycle week <day of the week>] : weekly cycle")
        print("-[cycle every <number of days> days, start <yyyy-mm-dd>] : cycle with specific period\n")

        print("Cycles are also indexed\n")

        print("-[show cycles] : shows all cycles")
        print("-[stop cycle <cycle index>] : removes cycle")


# [type, field1, field2, field3, field4]
# types: annual, monthly, weekly, manual diff
#        0       1        2       3
class Cycle:
    def __init__(self, data):
        self.type = data[0]
        self.field1 = data[1]
        self.field2 = data[2]
        self.field3 = data[3]
        self.field4 = data[4]
        self.text = data[5]

    def recycle(self):
        fields = [-1, -1, -1, -1, -1, ""]
        fields[0] = self.type
        fields[1] = self.field1
        fields[2] = self.field2
        fields[3] = self.field3
        fields[4] = self.field4
        fields[5] = self.text
        return(fields)

    def falls(self, date):
        if self.type == 0: # year
            return(self.field1 == date.month and self.field2 == date.day)
        elif self.type == 1: # month
            return(self.field1 == date.day)
        elif self.type == 2: # week
            return(weekDays[self.field1] == date.weekday())
        else:
            ancor = datetime.date(self.field1, self.field2, self.field3)
            return((date - ancor).days % self.field4 == 0)

def get_last(cycle):
    return(cycle[-1])

def _type(cycle):
    if cycle.type == 0:
        return(" [annual]")
    elif cycle.type == 1:
        return(" [monthly]")
    elif cycle.type == 2:
        return(" [weekly]")
    else:
        if cycle.field1 == 1:
            return(" [every day]")
        else:
            return(" [every " + str(cycle.field4) + " days]")

def ending(day):
    if day == 1 or day == 21 or day == 31:
        return("st")
    elif day == 2 or day == 22:
        return("nd")
    elif day == 3 or day == 23:
        return("rd")
    else:
        return("th")

def flatten(date):
    return(str(date.year) + '-' + norm(str(date.month)) + '-' + norm(str(date.day)))

def norm(a):
    if len(a) == 1:
        return '0' + a
    else:
        return a
