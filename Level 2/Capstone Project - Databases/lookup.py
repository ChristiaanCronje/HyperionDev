import sqlite3
import json
import xml.etree.ElementTree as ET

try:
    conn = sqlite3.connect("HyperionDev.db")
except sqlite3.Error:
    print("Please store your database as HyperionDev.db")
    quit()

cur = conn.cursor()

with open('create_database.sql', 'r') as sql_file:
    sql_script = sql_file.read()
    cur.executescript(sql_script)

def usage_is_incorrect(input, num_args):
    if len(input) != num_args + 1:
        print(f"The {input[0]} command requires {num_args} arguments.")
        return True
    return False


# This function stores query results in JSON format. 
# It first check if data exists, then extract column names from the 
# Cursor description. 
# The data is formatted as a list of dictionaries.
# Finally, the data is written to the specified file.
def store_data_as_json(data, filename):
    if not data or cur.description is None:
        print("No data to store.")
        return

    column_names = [desc[0] for desc in cur.description]

    data_list = [dict(zip(column_names, row)) for row in data]

    with open(filename, 'w') as f:
        json.dump(data_list, f, indent=4)

    print(f"Data saved to {filename} (JSON format).")

# These functions store query results in XML format. 
# They first check if data exists, then extract column names from the 
# Cursor description. 
# The data is formatted as an XML tree.
# Finally, the data is written to the specified file.
def store_data_as_xml(data, filename):
    if not data or cur.description is None:
        print("No data to store.")
        return

    column_names = [desc[0] for desc in cur.description]

    root = ET.Element("Results")

    for row in data:
        entry = ET.SubElement(root, "Entry")
        for col_name, col_value in zip(column_names, row):
            field = ET.SubElement(entry, col_name)
            field.text = str(col_value) if col_value is not None else ""

    tree = ET.ElementTree(root)
    tree.write(filename, encoding="utf-8", xml_declaration=True)

    print(f"Data saved to {filename} (XML format).")

def offer_to_store(data):
    while True:
        print("Would you like to store this result?")
        choice = input("Y/[N]? : ").strip().lower()

        if choice == "y":
            filename = input("Specify filename. Must end in .xml or .json: ")
            ext = filename.split(".")[-1]
            if ext == 'xml':
                store_data_as_xml(data, filename)
            elif ext == 'json':
                store_data_as_json(data, filename)
            else:
                print("Invalid file extension. Please use .xml or .json")

        elif choice == 'n':
            break

        else:
            print("Invalid choice")

usage = '''
What would you like to do?

d - demo
vs <student_id>            - view subjects taken by a student
la <firstname> <surname>   - lookup address for a given firstname and surname
lr <student_id>            - list reviews for a given student_id
lc <teacher_id>            - list all courses taken by teacher_id
lnc                        - list all students who haven't completed their course
lf                         - list all students who have completed their course and achieved 30 or below
e                          - exit this program

Type your option here: '''

print("Welcome to the data querying app!")

while True:
    print()
    user_input = input(usage).split(" ")
    print()

    command = user_input[0]
    if len(user_input) > 1:
        args = user_input[1:]

    if command == 'd': 
        data = cur.execute("SELECT * FROM Student")
        for _, firstname, surname, _, _ in data:
            print(f"{firstname} {surname}")
    
    # Retrieves all subjects for a given student by joining 
    # StudentCourse and Course on course_code.
    elif command == 'vs': 
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        data = None

        cur.execute(
        '''SELECT c.course_name FROM StudentCourse sc
           JOIN Course c ON sc.course_code = c.course_code
           WHERE sc.student_id = ?''',
        (student_id,)
        )
        
        data = cur.fetchall()
        for row in data:
            print(row[0]) 
        
        print() 

        offer_to_store(data)

    # Retrieves a student's street and city by joining Student
    # And Address on address_id.
    elif command == 'la':
        if usage_is_incorrect(user_input, 2):
            continue
        firstname, surname = args[0], args[1]
        data = None

        cur.execute(
        '''SELECT street, city FROM Address a
           JOIN Student s on s.address_id = a.address_id
           WHERE s.first_name = ? AND s.last_name = ?''',
        (firstname, surname)
        )

        data = cur.fetchall()
        for row in data:
            print(f"Street: {row[0]}, City: {row[1]}")
            
            print() 

        offer_to_store(data)
    
    # Retrieves all reviews for a specific student, displaying 
    # Completeness, efficiency, style, documentation, and review text.
    elif command == 'lr':
        if usage_is_incorrect(user_input, 1):
            continue
        student_id = args[0]
        data = None

        cur.execute(
        '''SELECT completeness, efficiency, style, documentation, review_text
           FROM Review
           WHERE student_id = ?''',
        (student_id, )
        )

        data = cur.fetchall()
        for row in data:
            print(f"completeness: {row[0]}\n"
                  f"efficiency: {row[1]}\n"
                  f"style: {row[2]}\n"
                  f"documentation: {row[3]}\n"
                  f"review_text: {row[4]}")
            
            print() 

        offer_to_store(data)
    
    # Lists students who haven't completed their course by joining 
    # Student, StudentCourse, and Course on student_id and course_code.
    elif command == 'lnc':
        data = None

        cur.execute(
        '''SELECT s.student_id, s.first_name, s.last_name, s.email, 
           c.course_name
           FROM Student s
           JOIN StudentCourse sc on sc.student_id = s.student_id
           JOIN Course c ON c.course_code = sc.course_code
           WHERE sc.is_complete = ?''',
        (0, )
        )

        data = cur.fetchall()
        for row in data:
            print(f"student id: {row[0]}\n"
                  f"first name: {row[1]}\n"
                  f"last name: {row[2]}\n"
                  f"email: {row[3]}\n"
                  f"course name: {row[4]}")
            
            print() 

        offer_to_store(data)
    
    # Lists students who completed their course with a mark of 30 or 
    # Below by joining Student, StudentCourse, and Course.
    elif command == 'lf':
        data = None

        cur.execute(
        '''SELECT s.student_id, s.first_name, s.last_name, s.email, 
           c.course_name, sc.mark
           FROM Student s
           JOIN StudentCourse sc on sc.student_id = s.student_id
           JOIN Course c ON c.course_code = sc.course_code
           WHERE sc.is_complete = ? and sc.mark <= ?''',
        (1, 30)
        )

        data = cur.fetchall()
        for row in data:
            print(f"student id: {row[0]}\n"
                  f"first name: {row[1]}\n"
                  f"last name: {row[2]}\n"
                  f"email: {row[3]}\n"
                  f"course name: {row[4]}\n"
                  f"mark: {row[5]}")
            
            print() 

        offer_to_store(data)

    # Retrieves all courses taught by a specific teacher by joining 
    # Course and Teacher on teacher_id.
    elif command == 'lc':
        data = None
        teacher_id = args[0]

        cur.execute(
        '''SELECT course_name
           FROM Course c
           JOIN Teacher t on c.teacher_id = t.teacher_id
           WHERE c.teacher_id = ?
           ''',
           (teacher_id, )
        )

        data = cur.fetchall()
        for row in data:
            print(f"{row[0]}") 

        print()

        offer_to_store(data)

    elif command == 'e':
        print("Programme exited successfully!")
        break
    
    else:
        print(f"Incorrect command: '{command}'")

conn.close()

print()