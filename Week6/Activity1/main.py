# This is the main module of the program, 
# which related to student login, assignment submission, and grade viewing.
from users import (
    student_login,
    submit_assignment,
    view_grades
)

# The main function of the program, which includes user activities.
def main():

    # Student logs into the system with decorated function to log the activity details.
    student_login("Mohammad")

    # Student submits an assignment with decorated function to log the activity details.
    submit_assignment(
        "Mohammad",
        "Python Decorator Project"
    )

    # Student views their grades with decorated function to log the activity details.
    # Here is logical error, the parameter should be "Mohammad" instead of "Alex" to be consistent with the previous activities.
    view_grades("Alex")

# The starting point of the program, which calls the main function to execute the sequence of tasks defined in main.
if __name__ == "__main__":
    main()
