#Importing the datetime module to get the current date and time for logging purposes
from datetime import datetime

# The log_activity decorator takes a function as an argument 
# and returns a wrapper function that adds logging functionality around the original function's execution.
def log_activity(func):

    # The wrapper function is defined inside log_activity and 
    # logs the execution details of any function it decorates, 
    # including the function name, execution time, 
    # and status messages before 
    # and after the function call.
    
    # * means that the wrapper function can accept any number of positional and keyword arguments,
    # which are then passed to the original function when it is called.

    # ** allows the wrapper to accept any keyword arguments,
    # which are also passed to the original function.
    def wrapper(*args, **kwargs):

        # print separator
        print("===================================")

        # print the name of the function being executed and the current time for logging purposes.
        print(f"Function: {func.__name__}")

        # print the current time to log when the activity started.
        print(f"Time: {datetime.now()}")

        # print a message indicating that the activity has started.
        print("Activity started...")

        # Call the original function with the provided arguments and store the result as None
        result = func(*args, **kwargs)

        # print a message indicating that the activity has completed.
        print("Activity completed.")

        # print separator to visually separate log entries for different activities.
        print("===================================\n")

        # return the result of the original function call, which is None in this case since the decorated functions do not return any value.
        return result

    return wrapper
