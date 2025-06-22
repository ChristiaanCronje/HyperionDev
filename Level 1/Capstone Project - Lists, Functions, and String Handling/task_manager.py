#=====importing libraries===========
'''This is the section where you will import libraries'''

from datetime import datetime 

import os

#====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file
    - Use a while loop to validate your user name and password
'''
# Loop through all the lines in user.txt to add all the usernames and
# Passwords to their respective lists
# Then makes a loop that asks the user to enter their username and 
# Password until it matches one of them in the lists
usernames = []
passwords = []

with open("user.txt", "r") as users_file:
    for lines in users_file:
        temp = lines.strip()
        temp = temp.split(", ")
        usernames.append(temp[0])
        passwords.append(temp[1])

login = False

while not login:
    login_username = input("Please enter your username: ")
    login_password = input("Please enter your password: ")

    if login_username in usernames:
        user_position = usernames.index(login_username)
        if passwords[user_position] == login_password:
            login = True
            break
    
    print("Incorrect username and/or password, try again")

def reg_user():
    if login_username == "admin":
        username = input("Please create a username: ")
        while username in usernames:
            username = input(
                "This username has already been taken, try again: "
            )

        password = input("Please create a password: ")
        password_confirmation = input("Please confirm your password: ")

        if password == password_confirmation:
            with open("user.txt", "a") as users_file:
                users_file.write(f"\n{username}, {password}") 
        else:
            print("Password does not match confirmation")
    else:
        print("Only the admin can register new users.")

def add_task():
    username_assigned = input(
        "Please enter the username of the person "
        "that is assigned to this task: "
    )
    task_title = input("Please enter the title of this task: ")
    task_description = input("Please enter a description of the task: ")
    task_due_date = input("Please input the due date of this task: ")
    current_date = datetime.now()
    current_date_str = current_date.strftime("%d %b %Y")
    task_completed = "No"

    with open("tasks.txt", "a") as tasks_file:
        tasks_file.write(
            f"\n{username_assigned}, {task_title}, " 
            f"{task_description}, {current_date_str}, "
            f"{task_due_date}, {task_completed}"
        )  

def view_all():
    with open("tasks.txt", "r") as tasks_file:
        for lines in tasks_file:
            temp = lines.strip()
            temp = temp.split(", ")
            print(f"""Task:                 {temp[1]}
Assigned to:          {temp[0]}
Date assigned:        {temp[3]}
Due date:             {temp[4]}
Task complete?        {temp[5]}
Task description:
{temp[2]}

"""
)    

def view_mine():
    with open("tasks.txt", "r") as tasks_file:
        for  index, lines in enumerate(tasks_file, start = 1):
            temp = lines.strip()
            temp = temp.split(", ")
            if temp[0] == login_username:
                print(f"""Task {index}:               {temp[1]}
Assigned to:          {temp[0]}
Date assigned:        {temp[3]}
Due date:             {temp[4]}
Task complete?        {temp[5]}
Task description:
{temp[2]}

"""
)
def edit_task():
    with open('tasks.txt', 'r') as tasks_file:
        tasks = tasks_file.readlines()

    task_action = int(input("""Do you want to:
1 - Mark the task as complete
2 - Edit the task
"""
))  
    for i, task in enumerate(tasks, start=1):
        if i == task_choice:
            temp = task.strip()
            temp = temp.split(", ")

            if task_action == 1:
                if temp[5] == "Yes":
                    print("Task already completed")
                else:
                    temp[5] = "Yes"
            else:
                if temp[5] == "No":
                    name = input("Enter who you want to assign this task to: ")
                    date = input("Enter the due date of the task: ")

                    temp[0] = name
                    temp[4] = date
                else:
                    print(
                        "Cannot edit task, because it has "
                        "already been completed"
                    )
            tasks[i - 1] = ", ".join(temp) + "\n"
            break

    with open("tasks.txt", "w") as tasks_file:
        tasks_file.writelines(tasks) 

def generate_task_overview():
    completed_task_count = 0
    incomplete_task_count = 0
    overdue_count = 0

    today = datetime.now()
    
    with open("tasks.txt", "r") as tasks_file:
        tasks = tasks_file.readlines()

    task_count = len(tasks)

    for task in tasks:
        temp = task.strip()
        temp = temp.split(", ")
        due_date = datetime.strptime(temp[4], "%d %b %Y")

        if temp[5].lower() == "yes":
            completed_task_count += 1
        else:
            incomplete_task_count += 1
            if due_date < today:
                overdue_count += 1

    percentage_incomplete = round(incomplete_task_count/
                                        task_count*100, 2)
    percentage_overdue = round(overdue_count/task_count*100, 2)

    with open("task_overview.txt", "w") as overview_file:
        overview_file.write(f"Total number of tasks: {task_count}\n")
        overview_file.write(
            f"Total number of completed tasks: {completed_task_count}\n"
        )
        overview_file.write(
            f"Total number of uncompleted tasks: {incomplete_task_count}\n"
        )
        overview_file.write(
            f"Total number of overdue tasks: {overdue_count}\n"
        )
        overview_file.write(
            f"Percentage of incomplete tasks: {percentage_incomplete}%\n"
        )
        overview_file.write(
            f"Percentage of overdue tasks: {percentage_overdue}%\n"
        )

def generate_user_overview():
    task_count = 0
    users = []
    user_stats = []
    today = datetime.now()

    with open('user.txt', 'r') as user_file:
        for user in user_file:
            temp = user.strip()
            temp = temp.split(", ")
            users.append(temp[0])

    user_count = len(users)

    for user in users:
        user_stats.append({
            "total_tasks": 0,
            "completed_tasks": 0,
            "uncompleted_tasks": 0,
            "overdue_tasks": 0,
        }) 
    
    with open("tasks.txt", "r") as tasks_file:
        tasks = tasks_file.readlines()

    task_count = len(tasks)

    for index, user in enumerate(users):
        for task in tasks:
            temp = task.strip()
            temp = temp.split(", ")
            due_date = datetime.strptime(temp[4], "%d %b %Y")

            if user == temp[0]:
                user_stats[index]['total_tasks'] += 1
                if temp[5] == 'Yes':
                    user_stats[index]['completed_tasks'] += 1       
                else:
                    user_stats[index]['uncompleted_tasks'] += 1  
                    if due_date < today:
                        user_stats[index]['overdue_tasks'] += 1  

    with open('user_overview.txt', "w") as overview_file:
        overview_file.write(f"Total number of users: {user_count}\n")
        overview_file.write(f"Total number of tasks: {task_count}\n\n")
   
        for index, user in enumerate(users):
            overview_file.write(f"{user}:\n")
            overview_file.write(
                f"Total number of tasks: "
                f"{user_stats[index]['total_tasks']}\n"
            )
            overview_file.write(
                f"Percentage of tasks assigned: "
                f"{round(user_stats[index]['total_tasks']/task_count*100, 2)}%"
                "\n"
            )
            overview_file.write(
                f"Percentage of of tasks that have been completed: "
                f"{round(user_stats[index]['completed_tasks'] / 
                         user_stats[index]['total_tasks']*100, 2)}%\n"
                )
            overview_file.write(
                f"Percentage of of tasks that must be completed: "
                f"{round(user_stats[index]['uncompleted_tasks'] / 
                         user_stats[index]['total_tasks']*100, 2)}%\n"
            )
            overview_file.write(
                f"Percentage of of tasks that are overdue: "
                f"{round(user_stats[index]['overdue_tasks'] / 
                         user_stats[index]['total_tasks']*100, 2)}%\n"
            )
            overview_file.write('\n')  

def display_statistics():
    if not (
        os.path.exists('task_overview.txt') 
        and os.path.exists('user_overview.txt')
    ):
        generate_task_overview()
        generate_user_overview()
    
    print("\nTask Overview:")
    with open('task_overview.txt', 'r') as task_overview_file:
        print(task_overview_file.read())

    print("\nUser Overview:")
    with open('user_overview.txt', 'r') as user_overview_file:
        print(user_overview_file.read())

while True:
    # Present the menu to the user and 
    # make sure that the user input is converted to lower case.
    menu_options = '''Select one of the following options:
r - register a user
a - add task
va - view all tasks
vm - view my tasks
'''

    if login_username == "admin":
        menu_options += "gr - generate reports\nds - display statistics\n"

    menu_options += "e - exit\n: "

    menu = input(menu_options).lower()
            
    # Asks the user to create a username and password if 'r' was typed
    # In and only register's the account if the logged in user is
    # The admin, the password was correctly
    # Confirmed and the username does notalready exist or else it will
    # Give an relevant error message. Then the program
    # Opens the user.txt file to append
    # The new username and password 
    if menu == 'r':
        '''This code block will add a new user to the user.txt file
        - You can use the following steps:
            - Request input of a new username
            - Request input of a new password
            - Request input of password confirmation.
            - Check if the new password and confirmed password are the same
            - If they are the same, add them to the user.txt file,
              otherwise present a relevant message''' 
        reg_user()
        
    # Asks the user to enter the details of a new task that needs to be
    # Completed if the user typed "a"
    # The program will then open tasks.txt textfile to append a task in
    # A new line 
    elif menu == 'a':
        '''This code block will allow a user to add a new task to task.txt file
        - You can use these steps:
            - Prompt a user for the following: 
                - the username of the person whom the task is assigned to,
                - the title of the task,
                - the description of the task, and 
                - the due date of the task.
            - Then, get the current date.
            - Add the data to the file task.txt
            - Remember to include 'No' to indicate that the task is not complete.'''
        add_task()
    
    # Outputs all the tasks that need to be completed if the user typed
    # "va". It does so by opening tasks.txt textfile and looping through
    # Each line and storing each bit of information in a list. Then it
    # Displays the information respectively
    elif menu == 'va':
        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         You can do it in this way:
            - Read a line from the file.
            - Split that line where there is comma and space.
            - Then print the results in the format shown in the Output 2 in the PDF
            - It is much easier to read a file using a for loop.'''
        view_all()
    
    # Outputs all the tasks of the logged in user that needs to be
    # Completed if the user typed
    # "vm". It does so by opening tasks.txt textfile and looping through
    # Each line and storing each bit of information in a list if the 
    # Person the task was assigned to matches the person logged in. Then
    # It displays the information respectively
    # Then it allows the user to select a specific task or "-1" if they
    # Want to return to the menu. You can either choose to change the
    # Task as being completed or change the person working on it with 
    # The due date only IF the task hasn't been completed
    elif menu == 'vm':
        '''This code block will read the task from task.txt file and
         print to the console in the format of Output 2 presented in the PDF
         You can do it in this way:
            - Read a line from the file
            - Split the line where there is comma and space.
            - Check if the username of the person logged in is the same as the 
              username you have read from the file.
            - If they are the same you print the task in the format of Output 2
              shown in the PDF '''
        view_mine()
        task_choice = int(input("Select a task number(-1 to return to menu): "))
        if not task_choice == -1:
            edit_task()

    # Make a function to extract information from "tasks.txt" to output 
    # To "task_overview" In a easy to read manner 
    # Make a function to extract information from "tasks.txt" and
    # "user.txt" to output to "user_overview.txt" In a easy to read 
    # manner
    # Generate 2 textfiles named "task_overview.txt" and "user_overview"
    # By calling both functions
    elif menu == 'gr' and login_username == "admin":
        generate_task_overview()
        generate_user_overview()

    # If 'ds' was entered and the logged in user is the admin, the 
    # Program will extract information from "user_overview.txt" and
    # "task_overview.txt" and display it
    # If the files "task_overview.txt" and "user_overview.txt" don't
    # Exist, call the functions to generate both textfiles           
    elif menu == 'ds' and login_username == "admin":
        display_statistics()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")
