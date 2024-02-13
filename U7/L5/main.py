from student import Student

student = Student(input("Enter student's name: "))

def add_course():
    course = input("Enter the name of the course: ")
    student.add_course(course)

def add_grade():
    print("Here are your courses:")
    available_courses = student.test_scores.keys()
    for course in available_courses:
        print(course)
    course = ""
    while course not in available_courses:
        course = input("Enter the name of the course you want to add grades to: ")
    input_grade = ""
    while input_grade != "-1":
        input_grade = input("Enter test score (-1 to finish): ")
        if input_grade != "-1":
            student.add_test(course, [int(input_grade)])

def get_averages():
    for course in student.test_scores:
        print(f"{course}: {student.get_average(course)}")

def quit():
    print("Goodbye!")
    exit()

menu_options = {
    "a": {
        "name": "Add a course",
        "function": add_course
    },
    "b": {
        "name": "Add a grade to a course",
        "function": add_grade
    },
    "c": {
        "name": "Get averages for all courses",
        "function": get_averages
    },
    "q": {
        "name": "Quit",
        "function": quit
    }
}

menu_choice = ""
while menu_choice != "q":
    for key in menu_options:
        print(f"Option {key}: {menu_options[key]['name']}")
    menu_choice = input("Choose your option: ")
    print()
    if menu_choice in menu_options:
        menu_options[menu_choice]["function"]()
        print()
    else:
        print("Invalid option\n")
