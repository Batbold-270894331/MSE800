#importing the log_activity decorator from the decorators module
from decorators import log_activity

#The student_login function is decorated with log_activity to print its execution details
# start with @ means that the function student_login is being decorated 
# with the log_activity decorator, 
# which will add logging functionality to it when it is called.
@log_activity
def student_login(username):
    print(f"{username} logged into the system.")

#The submit_assignment function is decorated with log_activity to ensure that its execution is logged.
@log_activity
def submit_assignment(username, assignment):
    print(f"{username} submitted {assignment}.")

#The view_grades function is decorated with log_activity to log when a user views their grades.
@log_activity
def view_grades(username):
    print(f"{username} is viewing grades.")