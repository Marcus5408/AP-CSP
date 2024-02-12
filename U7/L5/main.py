from student import Student

student = Student(input("Enter student's name: "))
user_input = ""
while user_input != "-1":
    user_input = input("Enter test score, -1 to quit: ")
    if user_input != "-1":
        student.add_test(int(user_input))

print(f"Student name: {student.name}")
print(f"Student test scores: {student.test_scores}")
print(f"Student average test score: {student.get_average()}")