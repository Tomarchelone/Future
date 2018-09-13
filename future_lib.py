import sys
import json
import datetime
from time import *
from datetime import *

from future_constants import *
from future_errors import *

# Exceptions

class Future:
    def __init__(self, data):
        self.window = data["window"]
        self.events = data["events"]
        self.cycles = list(
            map(lambda l: Cycle(l[0], l[1], l[2]), data["cycles"])
        )

    def show(self):
        events = self.events
        window = self.window
        cycles = self.cycles

        self.clean()

        base_len = self.print_future()

        today = datetime.today()
        index = -1
        for i in range(window):
            date = today + timedelta(days=i)
            flat_date = datetime.strftime(date, "%Y-%m-%d")

            header_printed = False
            if flat_date in events:
                self.print_header(i, date, base_len)
                header_printed = True

                for event in events[flat_date]:
                    index += 1
                    self.print_event(event, index, base_len)

            for (j, cycle) in enumerate(cycles):
                if cycle.falls(date):
                    if not header_printed:
                        self.print_header(i, date, base_len)
                        header_printed = True

                    self.print_cycle(cycle, j, base_len)

        #if header_printed:
        #    print("┣" + "━" * (base_len - 2) + "┫")

        self.print_foot(base_len)

    def add(self, args):
        events = self.events

        if len(args) != 3 or args[1] != 'to':
            print_add_format_error()
            return()

        flat_date = args[2]

        try:
            flat_date = datetime.strftime(
                datetime.strptime(
                    flat_date
                    , "%Y-%m-%d"
                )
                , "%Y-%m-%d"
            )
        except:
            print_incorrect_date_error()
            return()

        flat_today = datetime.strftime(datetime.today(), "%Y-%m-%d")
        if flat_date < flat_today:
            print_past_error()
            return()

        text = input()

        if flat_date not in events:
            events[flat_date] = []

        events[flat_date].append(text)

        print("Event added to", flat_date)

    def rm(self, args):
        if len(args) != 2:
            print_incorrect_rm_format_error()
            return()

        events = self.events

        try:
            index = int(args[1])
            order = sorted(events.keys())

            if index < 0:
                print_incorrect_index_error()
                return()

            j = -1
            for date in order:
                for event in events[date]:
                    j += 1
                    if j == index:
                        events[date].remove(event)
                        if not events[date]:
                            events.pop(date)

                        print("Ok")
                        return()

            if j < index:
                print_incorrect_index_error()
                return()

        except:
            print_incorrect_index_error()
            return()

    def cycle(self, args):
        if (len(args) != 3
            or args[1] not in ['annual', 'monthly', 'weekly', 'daily']):
            print_cycle_format_error()
            return()

        cycle_type = args[1]
        #print(cycle_type)
        flat_ancor = args[2]

        try:
            flat_ancor = datetime.strftime(
                datetime.strptime(
                    flat_ancor
                    , "%Y-%m-%d"
                )
                , "%Y-%m-%d"
            )
        except:
            print_incorrect_date_error()
            return()

        text = input()

        self.cycles.append(Cycle(cycle_type, flat_ancor, text))
        print("Ok")

    def stop_cycle(self, args):
        try:
            index = int(args[1])
            self.cycles.pop(index)
        except:
            print_incorrect_index_error()
            return()

        print("Ok")

    def set_window(self, args):
        if (args[1] == 'window'):
            try:
                window_size = int(input())
                assert window_size > 0
            except:
                print_window_error()
                return()

            self.window = window_size
            print("Window size is now equal to", window_size)

        else:
            print_set_error()
            return()

    def clean(self):
        flat_today = datetime.strftime(datetime.today(), "%Y-%m-%d")

        pop_list = []
        for flat_date in self.events:
            if flat_date < flat_today:
                pop_list.append(flat_date)

        for date in pop_list:
            self.events.pop(date)

    def print_cycles(self):
        for (j, cycle) in enumarate(self.cycles):
            print(cycle.text, " [", j, "] [", cycle.type, "]", sep='')

    def print_window(self):
        print("Window size is", self.window, "days")

    def print_future(self):
        main_header = ("┏━━━━━━━━┫Future for the next "
                       + str(self.window)
                       + " "
                       + day_s(self.window)
                       + "┣━━━━━━━━┓")

        base_len = len(main_header)
        # Это вычисление длины и положения крыши
        days_len = len(str(self.window)) + len(day_s(self.window))
        roof = "         ┏" + "━" * (21 + days_len) + "┓"
        bottom = "┃        ┗" + "━" * (21 + days_len) + "┛"
        bottom += " " * (base_len - 1 - len(bottom)) + "┃"

        print(roof)
        print(main_header)
        print(bottom)

        return(base_len)

    def print_header(self, i, date, base_len):
        date_str = datetime.strftime(date, "%Y-%m-%d")
        days_str = today_or_future(i)
        main_info = (date_str
                     + " │ "
                     + ind_to_day[date.weekday()]
                     + " │ "
                     + days_str
                     + " │")

        roof = ("┣"
                + "━" * (len(date_str) + 2)
                + "┯"
                + "━" * 5
                + "┯"
                + "━" * (len(days_str) + 2)
                + "┯"
                + "━" * (base_len - len(date_str) - len(days_str) - 14)
                + "┫")

        main_string = ("┃"
                       + " "
                       + main_info
                       + " " * (base_len - len(main_info) - 3)
                       + "┃")

        foot = ("┠"
                + "─" * (len(date_str) + 2)
                + "┴"
                + "─" * 5
                + "┴"
                + "─" * (len(days_str) + 2)
                + "┘")
        foot += " " * (base_len - len(foot) - 1) + "┃"

        print(roof)
        print(main_string)
        print(foot)

    def print_event(self, event, i, base_len):
        formatted_event = event + " [" + str(i) + "]"
        self.print_formatted_event(formatted_event, base_len)

    def print_cycle(self, cycle, j, base_len):
        formatted_cycle = cycle.text + " [" + cycle.cycle_type + "] [" + str(j) + "]"
        self.print_formatted_event(formatted_cycle, base_len)

    def print_formatted_event(self, formatted_event, base_len):
        word_list = list(formatted_event.split())

        current_line = ""
        dash = True
        for word in word_list:
            if (len(current_line) + len(word) < base_len - 4):
                current_line += word + " "
            else:
                print(dash_or_space(dash)
                    + current_line
                    + " " * (base_len - len(current_line) - 4)
                    + "┃"
                )
                current_line = word + " "
                dash = False

        if current_line:
            print(dash_or_space(dash)
                + current_line
                + " " * (base_len - len(current_line) - 4)
                + "┃"
            )

    def print_foot(self, base_len):
        print("┗" + "━" * (base_len - 2) + "┛" + "\n")

    def data(self):
        data = {}

        data["events"] = self.events
        data["cycles"] = list(map(lambda x: x.recycle(), self.cycles))
        data["window"] = self.window

        #print(data["cycles"])

        return(data)

    def help(self):
        print("Future")

        print("Commands description:\n")

        print("-[] : empty command (single 'future' word typed in terminal)"
               , "- view list of events.\n")

        print("-[add to <yyyy-mm-dd>] : add an event to date. After typing"
               , "the command press <Enter> and input description of the"
               , "event.\n")

        print("All events have indexes.\n")

        print("-[rm <index>] : rm event with given index.\n")

        print("There is a variable 'window' that represents the maximum"
               , "distance from today to the shown date. Dates that are farther"
               , "away in the future will not be shown until they are close"
               , "enough.\n")

        print("-[set window] : sets window size.\n")

        print("There is a special command for periodic events, 'cycle'.\n")
        print("There are four types of cycles:"
               , "'annual', 'monthly', 'weekly' and 'daily'.\n")

        print("-[cycle <cycle type> <yyyy-mm-dd>] : creates cycle.\n")
        print("After typing the command press <Enter> and"
               , "input description of the periodic event.")

        print("Cycles are also indexed.\n")

        print("-[show cycles] : show all cycles.")
        print("-[stop <cycle index>] : stop cycle.")

class Cycle:
    def __init__(self, cycle_type, flat_ancor, text):
        self.cycle_type = cycle_type
        self.flat_ancor = flat_ancor
        self.text = text

    def recycle(self):
        return([self.cycle_type, self.flat_ancor, self.text])

    def falls(self, date):
        if self.cycle_type == 'annual':
            ancor = datetime.strptime(self.flat_ancor, "%Y-%m-%d")
            return(ancor.month == date.month and ancor.day == date.day)

        elif self.cycle_type == 'monthly':
            ancor = datetime.strptime(self.flat_ancor, "%Y-%m-%d")
            return(ancor.day == date.day)

        elif self.cycle_type == 'weekly':
            ancor = datetime.strptime(self.flat_ancor, "%Y-%m-%d")
            return(ancor.weekday() == date.weekday())

        elif self.cycle_type == 'daily':
            return(True)

        else:
            print_cycle_type_error()

def day_s(diff):
    if diff == 1:
        return("day")
    else:
        return("days")

def today_or_future(i):
    if i == 0:
        return("TODAY")
    else:
        return(str(i) + " " + day_s(i))

def dash_or_space(dash):
    if dash:
        return("┠─ ")
        dash = False
    else:
        return("┃  ")
