# Check valid integer
def get_integer(message): 
    while True:
        try:
            value = int(input(message))

            if value > 0:
                return value

            print("Value must be greater than 0.")

        except ValueError:
            print("Please enter a valid integer.")

# Check Valid Marks

def get_marks(message):
    while True:
        try:
            marks = float(input(message))

            if 0 <= marks <= 100:
                return marks

            print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter valid numeric marks.")

# Check name

def get_name(message):
    while True:
        name = input(message).strip()

        if not name:
            print("Name cannot be empty.")
        elif not all(char.isalpha() or char.isspace() or char in "-'" for char in name):
            print("Name can contain only letters, spaces, hyphens, and apostrophes.")
        else:
            return name

# Check Course 

def get_course(message):
    while True:
        course = input(message).strip()

        if course:
            return course

        print("Course cannot be empty.")
