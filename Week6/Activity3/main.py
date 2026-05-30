def main():
    numbers = [1, 2, 3, 4, 5]
    squares = {str(x): x**2 for x in numbers}
    print(squares)
    print(type(squares))

def merge_dicts():
    # Dictionary 1
    student1 = {
        "name": "Alex",
        "age": 42,
        "course": "Data Analytics",
        "city": "Auckland",
        "status": "Lecturer"
    }
    
    # Dictionary 2
    student2 = {
        "name": "Sophia",
        "age": 29,
        "course": "Software Engineering",
        "city": "Wellington",
        "status": "Student"
    }
    
    # Dictionary 3
    student3 = {
        "name": "Michael",
        "age": 35,
        "course": "Cyber Security",
        "city": "Christchurch",
        "status": "Researcher"
    }

    # Add a student with the name containing "azw" to test the merging
    student4 = {
    "name": "Mazw", 
    "age": 26,
    "course": "Mathematics",
    "city": "Dublin",
    "status": "Tutor"
}

    # Group into a list
    all_students = [student1, student2, student3, student4]
    target_substring = "azw"

    # Initialize an empty dictionary for our final result
    merged_dict = {}

    for student in all_students:
        if target_substring.lower() in student.get("name", "").lower():
            # Merge the matching student into a new dict
            merged_dict = {**merged_dict, **student}

    print("--- Merged Dictionary ---")
    print(merged_dict)

if __name__ == "__main__":
    x, _, y = (10, 20, 30)

    print(f"x: {x}, y: {y}")
    print(_)

    #merge_dicts()