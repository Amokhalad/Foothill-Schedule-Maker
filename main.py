from coursefetch import *
from class_professor_obj import *



def get_user_classes():
    class_names = []  # list of strings
    while True:
        c_name = input("Enter Course Name or x to stop: ")
        if c_name == "x":
            print('Loading...')
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
                    if prof.class_teaching == sub_prof.class_teaching:
                        time_conflicts = True
                        break
                if not time_conflicts:
                    try:
                        not_duplicate = not sub_schedule or prof.dec_times[0][0] >= sub_schedule[-1].dec_times[0][0]
                    except IndexError:  # times has 'TBA' in there.
                        not_duplicate = not sub_schedule
                    if not_duplicate:
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
    sched_count = 0
    for schedule in schedules:
        print(f'Schedule {sched_count + 1}: ')
        for prof in schedule:
            print(f'\t {prof.class_teaching}: ')
            for i in range(len(prof.times)):
                print(f'\t\t{prof.name} -> {prof.times[i][0]} - {prof.times[i][1]} -> {prof.days[i]}')
        sched_count += 1


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
            ret_schedules.append(max_RMP_schedule(all_schedules))
        if choice == 2:
            ret_schedules.append(all_schedules)
    return ret_schedules


def print_result(schedules_list, scoring_user_decision):
    i = 0
    for choice in scoring_user_decision:
        if choice == 1:
            print('Largest Rating Schedules')
            print_schedules(schedules_list[i])
        if choice == 2:
            print('All Possible Schedules')
            print_schedules(schedules_list[i])
        i += 1


def main():
    print('WELCOME TO OPTIMAL SCHEDULE PROGRAM:\n')
    classes = get_user_classes()

    print('\nPick how you would like you like to score your schedule? ')
    scoring_user_decision = []
    while True:
        print('1: largest rating schedules')
        print('2: show all possible schedules')
        print('3: no nighest classes (coming soon)')
        print('4: avoid professor (coming soon)')
        print('0: Exit \n')
        try:
            user_choice = int(input("Enter choice: "))
        except ValueError:
            print('Enter Numbers Only')
            continue
        if user_choice == 0:
            break

        else:
            scoring_user_decision.append(user_choice)

    all_schedules = all_possible_schedules(classes, len(classes))
    print_result(score(all_schedules, scoring_user_decision), scoring_user_decision)


if __name__ == "__main__":
    main()
