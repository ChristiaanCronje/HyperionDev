#=====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import datetime 

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
users_file.close()

login = False

while login == False:
    login_username = input("Please enter your username: ")
    login_password = input("Please enter your password: ")

    if login_username in usernames:
        pos_user = usernames.index(login_username)
    if login_password in passwords:
        pos_pass = passwords.index(login_password)
        
    if (
        login_username in usernames 
        and login_password in passwords
        and pos_user == pos_pass
    ):
        login = True
    else:
        print("Incorrect username and/or password, try again")


while True:
    # Present the menu to the user and 
    # make sure that the user input is converted to lower case.
    if login_username == "admin":
        menu = input('''Select one of the following options:
    r - register a user
    a - add task
    va - view all tasks
    vm - view my tasks
    ds - display statistics
    e - exit
    : ''').lower()
    else:
        menu = input('''Select one of the following options:
    r - register a user
    a - add task
    va - view all tasks
    vm - view my tasks
    e - exit
    : ''').lower()
    # Asks the user to create a username and password if 'r' was typed
    # In and only register's the account if the logged in user is
    # The admin and the password was correctly
    # Confirmed or else it will give an error message. Then the program
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
        if login_username == "admin":
            username = input("Please create a username: ")
            password = input("Please create a password: ")
            password_confirmation = input("Please confirm your password: ")

            if password == password_confirmation:
                with open("user.txt", "a") as users_file:
                    users_file.write(f"\n{username}, {password}")
                users_file.close()    
            else:
                print("Password does not match confirmation")
        else:
            print("Only the admin can register new users.")

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
        username_assigned = input("Please enter the username of the person " 
                                  "that is assigned to this task: ")
        task_title = input("Please enter the title of this task: ")
        task_description = input("Please enter a description of the task: ")
        task_due_date = input("Please input the due date of this task: ")
        # Learned the datetime from the datetime module from my uncle
        # Beyers cronje
        current_date = datetime.now()
        formatted_current_date = current_date.strftime("%d %b %Y")
        task_completed = "No"

        with open("tasks.txt", "a") as tasks_file:
            tasks_file.write(f"\n{username_assigned}, {task_title}, " 
                             f"{task_description}, {formatted_current_date}, "
                             f"{task_due_date}, {task_completed}")
        tasks_file.close()
    
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
        with open("tasks.txt", "r") as tasks_file:
            for lines in tasks_file:
                temp = lines.strip()
                print(temp)
                temp = temp.split(", ")
                temp[0] = "chris"
                print(f"""Task:                 {temp[1]}
Assigned to:          {temp[0]}
Date assigned:        {temp[3]}
Due date:             {temp[4]}
Task complete?        {temp[5]}
Task description:
{temp[2]}

"""
)
        tasks_file.close()    
    # Outputs all the tasks of the logged in user that needs to be
    # Completed if the user typed
    # "vm". It does so by opening tasks.txt textfile and looping through
    # Each line and storing each bit of information in a list if the 
    # Person the task was assigned to matches the person logged in. Then
    # It displays the information respectively
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
        with open("tasks.txt", "r") as tasks_file:
            for lines in tasks_file:
                temp = lines.strip()
                temp = temp.split(", ")
                if temp[0] == login_username:
                    print(f"""Task:                 {temp[1]}
Assigned to:          {temp[0]}
Date assigned:        {temp[3]}
Due date:             {temp[4]}
Task complete?        {temp[5]}
Task description:
{temp[2]}

"""
)
        tasks_file.close()

    # If 'ds' was entered and the logged in user is the admin, the 
    # Program will loop through the tasks.txt and user.txt textfiles
    # And count the number of lines there are that corresponds to the
    # Number of tasks and users
    # Then it will displat them to the user                
    elif menu == 'ds' and login_username == "admin":
        total_tasks = 0
        total_users = 0
        with open("tasks.txt", "r") as tasks_file:
            for lines in tasks_file:   
                total_tasks += 1 
        tasks_file.close()

        with open("user.txt", "r") as user_file:
            for lines in user_file:   
                total_users += 1 
        user_file.close()
        print()
        print(f"Total number of tasks: {total_tasks}")
        print(f"Total number of users: {total_users}")
        print()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have entered an invalid input. Please try again")