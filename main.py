from coursefetch import *
import copy


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


def get_user_classes():
    class_names = []  # list of strings
    while True:
        c_name = input("Enter Course Name or x to stop: ")
        if c_name == "x":
            break
        else:
            class_names.append(c_name)

    classes_data = [get_courses_from_input(course)[0] for course in class_names]
    classes = [Class(classes_data[i], class_names[i]) for i in range(len(class_names))]
    return classes


def all_possible_schedules(classes, num_of_classes):
    if num_of_classes == 0:
        return [[]]

    schedules = []
    sub_schedules = all_possible_schedules(classes, num_of_classes - 1)

    for sub_schedule in sub_schedules:
        for cls in classes:
            for prof in cls.prof_list:
                time_conflicts = False
                for sub_prof in sub_schedule:
                    if has_time_conflict(sub_prof, prof):
                        time_conflicts = True
                        break
                if not time_conflicts:
                    not_duplicate = not sub_schedule or prof.dec_times[0][0] >= sub_schedule[-1].dec_times[0][0]
                    not_same_class = not sub_schedule or prof.class_teaching != sub_schedule[-1].class_teaching
                    if not_duplicate and not_same_class:
                        schedules.append(sub_schedule + [prof])
    return schedules


def has_time_conflict(profA, profB):
    same_days = False

    for days_a in profA.days:
        for days_b in profB.days:
            if days_a == 'TBA' or days_b == 'TBA':
                continue
            for day in days_a:
                if day in days_b:
                    same_days = True
    if same_days:
        for time_a in profA.dec_times:
            for time_b in profB.dec_times:
                if time_a == 'TBA' or time_b == 'TBA':
                    continue
                if (time_a[0] < time_b[1]) and (time_a[1] > time_b[0]):
                    return True
    else:
        return False


def prints(classes):
    for cls in classes:
        print(cls.cls_name)
        for prof in cls.prof_list:
            print(f'\t {prof.name} -> {prof.times} -> {prof.days}')

        print('\n')


def print_schedules(schedules):
    i = 0
    for sched in schedules:
        print(f'Schedule {i + 1}: ')
        print_sched(sched)
        i += 1


def print_sched(schedule):
    for prof in schedule:
        print(f'\t {prof.class_teaching}: {prof.name} -> {prof.times} -> {prof.days}')


def max_RMP_schedule(all_schedules):
    max_rmp = 0
    # finding the max_rmp
    schedules_with_max_rmp = []
    for schedule in all_schedules:
        rmp_sum = 0
        for prof in schedule:
            rmp_sum += prof.rating
        if max_rmp <= rmp_sum:
            max_rmp = rmp_sum

    # finding the schedules with the max_rmp

    for schedule in all_schedules:
        rmp_sum = 0
        for prof in schedule:
            rmp_sum += prof.rating
        if max_rmp == rmp_sum:
            schedules_with_max_rmp.append(schedule)

    return schedules_with_max_rmp


def score(all_schedules, scoring_user_decision):
    ret_schedules = []
    for choice in scoring_user_decision:
        if choice == 1:
            ret_schedules = max_RMP_schedule(all_schedules)

    return ret_schedules


def main():
    print('WELCOME TO OPTIMAL SCHEDULE PROGRAM:\n')
    print('Pick how you would like you like to score your schedule? ')
    scoring_user_decision = []
    while True:
        print('1: largest RMP rating')
        print('2: no nighest classes (coming soon)')
        print('3: avoid professor (coming soon)')
        print('0: Exit \n')

        user_choice = int(input("Enter choice: "))

        if user_choice == 0:
            break
        else:
            scoring_user_decision.append(user_choice)

    classes = get_user_classes()
    all_schedules = all_possible_schedules(classes, len(classes))
    print_schedules(score(all_schedules, scoring_user_decision))


if __name__ == "__main__":
    main()
