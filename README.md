# StudentFlow – Student Management System

A web-based Student Management System built using Python and Flask. It provides an easy-to-use dashboard to manage student records, academic performance, grades, and reports.

## Features

- Add new student records
- View all registered students
- Search students by roll number or name
- Update student information
- Delete student records
- Input and manage subject marks
- Automatically calculate total marks and average
- Generate grades based on academic performance
- Sort and rank students by academic performance
- Filter students by pass/fail status
- Export student records to CSV
- Input validation and duplicate roll number checking
- JSON-based data storage

## Technologies Used

- **Python** – Backend programming
- **Flask** – Web framework
- **HTML** – Webpage structure
- **CSS** – Styling and layout
- **JavaScript** – Frontend interactions
- **JSON** – Data storage

## Project Structure

```text
StudentFlow/
│
├── app.py
├── student.py
├── s_management.py
├── validation.py
├── students.json
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/aka-shekhar/studentflow.git
```

### 2. Navigate to the project directory

```bash
cd studentflow
```

### 3. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

**Windows:**
```bash
.venv\Scripts\activate
```

### 5. Install Flask

```bash
pip install flask
```

### 6. Run the application

```bash
python app.py
```

Open the local URL displayed in your terminal (usually `http://127.0.0.1:5000/`) in your browser.

## Data Storage

Student records are stored in `students.json`. The application uses JSON file handling to save and retrieve student information.

## Future Improvements

- Database integration using SQLite or MySQL
- User authentication and role-based access
- Improved dashboard analytics
- Deployment to a cloud hosting platform

## Author

**Shekhar Prasad Bhatt**

GitHub: [@aka-shekhar](https://github.com/aka-shekhar)

---

*Developed as a learning project to practice Python, Flask, and web development.*
