def convert_time(time):  # helper function for convert_time in Professor class
    hour = int(time[0:2])
    minute = int(time[3:6])
    period = time[6:8]
    if period == "PM" and hour >= 1 and hour != 12:
        hour += 12
    elif hour == 12 and period == "AM":
        hour = 0

    return hour + (minute * (1.0 / 60.0))


class Professor:
    def __init__(self, name, days=None, times=None, rating=None, class_teaching=None):
        self._name = name
        self._days = days
        self._times = times
        self._decimal_times = copy.deepcopy(self._times)
        self._rating = rating
        self._class_teaching = class_teaching
        self.time_to_decimal()
        self.change_thursdays()

    @property
    def name(self):
        return self._name

    @property
    def times(self):
        return self._times

    @property
    def dec_times(self):
        return self._decimal_times

    @property
    def days(self):
        return self._days

    @property
    def rating(self):
        return self._rating

    @property
    def class_teaching(self):
        return self._class_teaching

    def time_to_decimal(self):
        for time in self._decimal_times:
            if time[0] == 'TBA' or time[1] == 'TBA':
                self._decimal_times.remove(time)
                continue
            time[0] = convert_time(time[0])  # start time
            time[1] = convert_time(time[1])  # end time

    def change_thursdays(self):
        # this function changes all Th to R
        for idx, day in enumerate(self._days):
            self._days[idx] = day.replace('Th', 'R')


class Class:
    def __init__(self, classes_data, class_name):
        self._data = classes_data
        self._class_name = class_name
        self.professors = []
        self.fill_professors_data()

    @property
    def cls_name(self):
        return self._class_name

    @property
    def prof_list(self):
        return self.professors

    def fill_professors_data(self):

        for prof in self._data:
            name = prof['times'][0]['instructor'][0]  # prof name
            days = []
            times = []
            for lecture in prof['times']:
                days.append(lecture['days'])  # prof days
                start_time = lecture['start_time']
                end_time = lecture['end_time']
                times.append([start_time, end_time])  # prof times
                rating = prof['rating']
                class_teaching = prof['dept'] + " " + prof['course']
                self.professors.append(Professor(name, days, times, rating, class_teaching))