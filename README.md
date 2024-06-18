WARNING: This does not work anymore due to the opencourse API no longer being maintained.



# Optimal Schedule Maker for Foothill College Students
        Author: Mokhalad Aljuboori

This will create a class schedule for a Foothill student using data from the course schedule and RateMyProfessor in order to achieve an optimal schedule.

This is a remake of my C++ program: https://github.com/ogvenocity/Class-Schedule
but written in python and with a file, `coursefetch.py` so that professor data is not manually inputted.

coursefetch.py is used from: https://github.com/LordOfDeadbush/autoschedule/blob/main/coursefetch.py


## How To use:
- clone repository
- before you run main.py
- input in terminal: `python -m pip install requests` to install requests
- run main.py
- when it asks you to enter a course name: 
        - enter the dept followed by the course number, like: Math 1A, or math 1D, or phYs 4C, Engl 1A, etc.... (caps don't matter)

## TODO:
- Add error checking
- optimze `all_possible_schedules()` function
- add other scoring functions
- improve user interface
