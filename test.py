sections = ['apple', 'avocado', 'banana', 'brocolli', 'coconut', 'cherry']


def has_no_conflict(c1, c2):
    return c1[0] != c2[0]  # 1st letters are different


def _all(iterable):
    for x in iterable:
        if not x:
            return False
    return True


def all_schedules(sections, num_sections):
    if num_sections == 0:
        return [[]]

    schedules = []
    sub_schedules = all_schedules(sections, num_sections - 1)
    # print('NUTELLA', sub_schedules)
    for sub_schedule in sub_schedules:
        for c in sections:
            no_conflicts = True
            for sub_c in sub_schedule:
                if not has_no_conflict(sub_c, c):
                    no_conflicts = False
                    break
            if no_conflicts and (not sub_schedule or c >= sub_schedule[-1]):
                schedules.append(sub_schedule + [c])
            # if all(has_no_conflict(sub_c, c) for sub_c in sub_schedule):
            #   schedules.append(sub_schedule + [c])
    return schedules


for num_sections in range(4):
    print(num_sections)
    print(all_schedules(sections, num_sections))
    print()
