
import json
from student import Student
from validation import get_marks
import os

class StudentManagementSystem:
    def __init__(self):
        self.students = []
        self.filename = os.path.join(os.path.dirname(__file__), 'students.json')

    def save_students(self): #Save details on file
        data = []

        for student in self.students:
            data.append({
                "roll_number": student.roll_number,
                "name": student.name,
                "age": student.age,
                "course": student.course,
                "marks": student.marks
            })

        with open(self.filename, "w") as file:
            json.dump(data, file, indent=4)

        print("Student records saved!")

        # Load data
    def load_students(self):
        try:
            with open(self.filename, "r") as file:
                data = json.load(file)

            for item in data:
                student = Student(
                    item["roll_number"],
                    item["name"],
                    item["age"],
                    item["course"],
                    item["marks"]
                )
                self.students.append(student)

            print("Student records loaded!")

        except FileNotFoundError:
            print("No saved records found. Starting fresh.")

        except json.JSONDecodeError:
            print("The JSON file is empty or invalid.")

        # Add new student data

    def add_student(self, student):
        for s in self.students:
            if s.roll_number == student.roll_number:
                print("Roll number already exists!")
                return

        self.students.append(student)
        self.save_students()
        print("Student added successfully!")

        # View student details

    def view_students(self):
        if not self.students:
            print("No student records found.")
            return

        for student in self.students:
            student.display()

        #Search student by roll number

    def search_student(self, roll_number):
        for student in self.students:
            if student.roll_number == roll_number:
                student.display()
                return

        print("Student not found.")

        # Search Details By Name

    def search_by_name(self, name):
        found = False

        for student in self.students:
            if name.lower() in student.name.lower():
                student.display()
                found = True

        if not found:
            print("Student not found.")

    # Generate Report Card

    def generate_report_card(self, roll_number):
        for student in self.students:
            if student.roll_number == roll_number:
                student.report_card()
                return

        print("Student not found.")

        # Update student data

    def update_student(self, roll_number):
        for student in self.students:
            if student.roll_number == roll_number:
                print("Leave a field blank to keep its current value.")

                name = input(f"New name ({student.name}): ")
                age = input(f"New age ({student.age}): ")
                course = input(f"New course ({student.course}): ")

                if name.strip():
                    student.name = name

                if age.strip():
                    try:
                        student.age = int(age)
                    except ValueError:
                        print("Invalid age. Age unchanged.")

                if course.strip():
                    student.course = course

                update_marks = input("Do you want to update marks? (y/n): ").strip().lower()

                if update_marks == "y":
                    new_marks = []

                    for i in range(3):
                        mark = get_marks(f"New marks for subject {i + 1}: ")
                        new_marks.append(mark)

                    student.marks = new_marks

                self.save_students()
                print("Student updated successfully!")
                return

        print("Student not found.")

        # delete student data

    
    def delete_student(self, roll_number):
        for student in self.students:
            if student.roll_number == roll_number:
                print("\nStudent found:")
                student.display()

                confirm = input(
                    "Are you sure you want to delete this student? (y/n): "
                ).strip().lower()

                if confirm == "y":
                    self.students.remove(student)
                    self.save_students()
                    print("Student deleted successfully!")
                else:
                    print("Deletion cancelled.")

                return

        print("Student not found.")

    # Check duplicate

    def roll_exists(self, roll_number):
        for student in self.students:
            if student.roll_number == roll_number:
                return True

        return False

    # Sort students

    def sort_students_by_marks(self):
        if not self.students:
            print("No students available.")
            return

        sorted_students = sorted(
            self.students,
            key=lambda student: student.total_marks(),
            reverse=True
        )

        for student in sorted_students:
            student.display()
            print("--------------------")

        # Student Ranking

    def show_student_rankings(self):
        if not self.students:
            print("No students available.")
            return

        ranked_students = sorted(
            self.students,
            key=lambda student: student.total_marks(),
            reverse=True
        )

        print("\n===== STUDENT RANKINGS =====")

        for rank, student in enumerate(ranked_students, start=1):
            print(
                f"Rank {rank}: {student.name} - "
                f"Total Marks: {student.total_marks()}"
            )

        # Statistics

    def show_class_statistics(self):
        if not self.students:
            print("No students available.")
            return

        totals = [
            student.total_marks()
            for student in self.students
        ]

        print("\n===== CLASS STATISTICS =====")
        print("Total Students:", len(self.students))
        print("Class Average:", sum(totals) / len(totals))
        print("Highest Marks:", max(totals))
        print("Lowest Marks:", min(totals))