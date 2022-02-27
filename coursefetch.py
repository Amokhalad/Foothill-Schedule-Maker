import requests


def format_input(input):  # input should be formatted as "MATH 1A,PSYCH 2B..."
    classes = input.split(",")  # seperates multiple course names
    classes = [i.split(" ") for i in classes]  # seperates MATH from 1A
    return classes


def remove_middle_name(fullName):
    name = fullName.split(" ")
    newName = name[0] + " " + name[-1]
    # print(newName)
    return newName


def get_RMP(teacher):
    teacher = remove_middle_name(teacher)
    teacher = teacher.replace(" ", "%20")
    r = requests.get("https://www.ratemyprofessors.com/search/teachers?query=" + teacher + "&sid=U2Nob29sLTE1ODE=")
    s = r.text
    index = s.find("avgRating")
    if index == -1:  # delete middle name, try again
        return 0
    if s[index + 11] == '0':
        return 0
    try:
        rating = float(s[index + 11:index + 14])  # if this doesn't work return 0
    except ValueError:
        try:
            rating = float(s[index + 11])
        except ValueError:
            return 0
    return rating


def get_course_info(crn):  # gets all course info and returns in dictionary
    r = requests.get("https://opencourse.dev/fh/classes/" + str(crn))
    info = r.json()  # look at the opencourse API for more info (or just go to the link and look at the formatting)
    return info  # return a dictionary with course data


def get_courses(name):  # gets all crns and calls course info for each one
    # name should be a list with [0] being the department and [1] being the course (e.g. ["MATH", "1A"])
    r = requests.get("https://opencourse.dev/fh/depts/" + name[0].upper() + "/courses/" + name[1].upper())
    data = r.json()
    coursedata = [get_course_info(i) for i in data["classes"]]
    for i in coursedata:
        rating = get_RMP(i['times'][0]['instructor'][0])  # TODO: fix this its not working aaaaaaaaaaaa
        i.update({"rating": rating})
    return coursedata


def get_courses_from_input(s):
    input = format_input(s)
    output = [get_courses(i) for i in input]
    return output

