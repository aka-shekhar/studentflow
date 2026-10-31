
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from s_management import StudentManagementSystem
from student import Student
import re
import csv
import io

app = Flask(__name__)
app.secret_key = "student-management-secret"

# Create our existing student management object
sms = StudentManagementSystem()

# Load saved student records
sms.load_students()


@app.route("/")

def home():
    sorted_students = sorted(
        sms.students,
        key=lambda student: str(student.roll_number)
    )
    ranked_students = sorted(
    sms.students,
    key=lambda student: student.calculate_avg(),
    reverse=True
)
    total_students = len(sms.students)
    passed_students = sum(
        1 for student in sms.students
        if student.calculate_grade() != "F"
    )

    failed_students = total_students - passed_students
    if total_students > 0:
        average_marks = sum(
            student.calculate_avg() for student in sms.students
        ) / total_students

        top_student = max(
            sms.students,
            key=lambda student: student.calculate_avg()
        )
    else:
        average_marks = 0
        top_student = None

    return render_template(
    "index.html",
    total_students=total_students,
    students=sorted_students,
    average_marks=round(average_marks, 2),
    top_student=top_student,
    passed_students=passed_students,
    failed_students=failed_students,
    ranked_students=ranked_students
)

def add_form_error(message):
    flash(message, "error")

    total = len(sms.students)
    passed = sum(
    1 for s in sms.students if s.calculate_grade() != "F"
    )
    failed = total - passed
    average = (
        sum(s.calculate_avg() for s in sms.students) / total
        if total else 0
    )

    top = max(
        sms.students,
        key=lambda s: s.calculate_avg(),
        default=None
    )

    return render_template(
        "index.html",
        total_students=total,
        students=sorted(sms.students, key=lambda s: str(s.roll_number)),
        average_marks=round(average, 2),
        top_student=top,
        form_data=request.form,
        passed_students=passed,
        failed_students=failed,
        show_form=True
    ), 400
def edit_form_error(message, student):
    flash(message, "error")

    return render_template(
        "edit.html",
        student=student,
        form_data=request.form
    ), 400

@app.route("/add", methods=["POST"])
def add_student():
    roll_number = request.form.get("roll_number", "").strip()
    name = request.form.get("name", "").strip()
    age = request.form.get("age", "").strip()
    course = request.form.get("course", "").strip()

    marks = [
        request.form.get(f"mark{i}", "").strip()
        for i in range(1, 4)
    ]

    # Check empty fields
    if not all([roll_number, name, age, course]) or any(m == "" for m in marks):
        return add_form_error("All fields are required!")

    # Validate student name
    if not re.fullmatch(r"[A-Za-z .'-]+", name):
        return add_form_error("Invalid student name!")

    # Validate course
    if not re.fullmatch(r"[A-Za-z0-9 .&()\-]+", course):
        return add_form_error("Invalid course name!")

    # Validate roll number
    if not roll_number.isdigit():
        return add_form_error("Roll number must contain only numbers!")
    
    # Check empty fields
    if not all([roll_number, name, age, course]) or any(
        mark == "" for mark in marks
    ):
        return "All fields are required!", 400

    # Convert and validate values
    try:
        age = int(age)
        marks = [float(mark) for mark in marks]

        if age <= 0 or any(mark < 0 or mark > 100 for mark in marks):
            return "Enter a valid age and marks between 0 and 100.", 400

    except ValueError:
        return "Age must be an integer and marks must be numeric.", 400

    # Create student object
    student = Student(roll_number, name, age, course, marks)

    # Check duplicate roll number
    for existing in sms.students:
        if str(existing.roll_number).strip() == roll_number:
            return add_form_error("Roll number already exists!")

    # Save student
    sms.add_student(student)

    flash("Student added successfully!", "success")
    return redirect(url_for("home"))

@app.route("/delete/<roll_number>", methods=["POST"]) # Delete data
def delete_student(roll_number):

    for student in sms.students:
        if str(student.roll_number) == roll_number:
            sms.students.remove(student)
            sms.save_students()

            flash("Student deleted successfully!", "success")
            return redirect(url_for("home"))

    flash("Student not found!", "error")
    return redirect(url_for("home"))

@app.route("/edit/<roll_number>") # Edit data
def edit_student(roll_number):

    for student in sms.students:
        if str(student.roll_number) == roll_number:
            return render_template(
                "edit.html",
                student=student
            )

    flash("Student not found!", "error")
    return redirect(url_for("home"))

@app.route("/update/<roll_number>", methods=["POST"]) # Update data
def update_student(roll_number):

    for student in sms.students:

        if str(student.roll_number) == roll_number:

            name = request.form.get("name", "").strip()
            age = request.form.get("age", "").strip()
            course = request.form.get("course", "").strip()

            marks = [
                request.form.get(f"mark{i}", "").strip()
                for i in range(1, 4)
            ]

            # Check empty fields
            if not name or not age or not course or any(m == "" for m in marks):
                flash("All fields are required!", "error")
                return redirect(url_for("edit_student", roll_number=roll_number))

            # Validate numeric values
            try:
                age = int(age)
                marks = [float(mark) for mark in marks]

            except ValueError:
                return edit_form_error(
                    "Age and marks must be numeric!", student
                )


            # Validate ranges
            if age <= 0 or any(mark < 0 or mark > 100 for mark in marks):
                return edit_form_error(
                    "Invalid age or marks! Marks must be between 0 and 100.",
                    student
                )


            # Validate course
            if not re.fullmatch(r"[A-Za-z0-9 .&()\-]+", course):
                return edit_form_error("Invalid course name!", student)


            # Validate name
            if not re.fullmatch(r"[A-Za-z .'-]+", name):
                return edit_form_error("Please enter a valid student name!", student)

            # Update student
            student.name = name
            student.age = age
            student.course = course
            student.marks = marks

            sms.save_students()

            flash("Student updated successfully!", "success")
            return redirect(url_for("home"))

    flash("Student not found!", "error")
    return redirect(url_for("home"))

    
@app.route("/export")
def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)

    # CSV column headings
    writer.writerow([
        "Roll Number", "Name", "Age", "Course",
        "Subject 1", "Subject 2", "Subject 3",
        "Total Marks", "Average", "Grade", "Status"
    ])

    # Write student records
    for student in sorted(
        sms.students,
        key=lambda s: int(s.roll_number)
    ):
        grade = student.calculate_grade()

        writer.writerow([
            student.roll_number,
            student.name,
            student.age,
            student.course,
            *student.marks,
            student.total_marks(),
            round(student.calculate_avg(), 2),
            grade,
            "Failed" if grade == "F" else "Passed"
        ])

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=student_records.csv"
    response.headers["Content-Type"] = "text/csv"

    return response

if __name__ == "__main__":
    app.run(debug=True)
