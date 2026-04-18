class Student:
    def __init__(self, name, age, studentId):
        self.name = name
        self.age = age
        self.studentId = studentId

    def GetData(self):
        return f"Name: {self.name}, Age: {self.age}, Student ID: {self.studentId}"

def CollectStudentData():
    print("Enter student data for at least 3 students:")

    count = 0
    students = []

    while True:
        name = input("Name: ")

        age = int(input("Age: "))
        studentId = input("ID: ")
        students.append(Student(name, age, studentId))
        count += 1

        if count >= 3:
            choice = input("Add another student? (Y/N): ").strip().lower()

            if choice != 'y':
                print("Finished collecting student data.")
                break

    return students

def DisplayStudentData(students):
    print(f"\nStudent data (sorted by age), you have {len(students)} students:")

    for student in sorted(students, key=lambda s: s.age):
        print(student.GetData())

if __name__ == "__main__":
    students = CollectStudentData()
    DisplayStudentData(students)