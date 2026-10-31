
class Student:
    def __init__(self, roll_number, name, age, course, marks):
        self.roll_number = roll_number
        self.name = name
        self.age = age
        self.course = course
        self.marks = marks

    def total_marks(self):
        return sum(self.marks)

    def calculate_avg(self):
        if not self.marks:
            return 0
        return self.total_marks() / len(self.marks)

    def calculate_grade(self):
         # Fail if any subject mark is below 35
        if any(mark < 40 for mark in self.marks):
            return 'F'
        avg = self.calculate_avg()

        if avg >= 90:
            return 'A+'
        elif avg >= 80:
            return 'A'
        elif avg >= 70:
            return 'B+'
        elif avg >= 60:
            return 'B'
        elif avg >= 50:
            return 'B-'
        elif avg >= 40:
            return 'C'
        else:
            return 'F'
    
    def report_card(self):
        print("\n========== STUDENT REPORT CARD ==========")
        print(f"Roll Number : {self.roll_number}")
        print(f"Name        : {self.name}")
        print(f"Course      : {self.course}")
        print("-----------------------------------------")

        for i, mark in enumerate(self.marks, start=1):
            print(f"Subject {i}   : {mark}")

        print("-----------------------------------------")
        print(f"Total Marks : {self.total_marks()}")
        print(f"Average     : {self.calculate_avg():.2f}")
        print(f"Grade       : {self.calculate_grade()}")
        print("=========================================")


    def display(self):
        print("\n--- Student Details ---")
        print("Roll Number:", self.roll_number)
        print("Name:", self.name)
        print("Age:", self.age)
        print("Course:", self.course)
        print("Marks:", self.marks)
        print("Total Marks:", self.total_marks())
        print("Average:", round(self.calculate_avg(), 2))
        print("Grade:", self.calculate_grade())
