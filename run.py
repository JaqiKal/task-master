import datetime  # From www.geeksforgeeks.org/python-datetime-module/
import gspread  # From love_sandwiches
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Google Sheets setup
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("task-master-database")
# worksheet = SHEET.worksheet('taskdb')
worksheet = SHEET.worksheet('test-sheet')


class ExitToMainMenu(Exception):
    """
    Amended from: stackoverflow.com/questions/1319615/
    proper-way-to-declare-custom-exceptions-in-modern-python

    Exception used to signal an exit back to the main menu.
    """
    pass


def get_user_input(prompt, normalize=False, allowed_values=None):
    """
    Amended from: www.geeksforgeeks.org/string-capitalize-python/

    Prompts the user for input and allows exit to the main menu
    upon receiving a specific input. If 'normalize' is True,
    it will capitalize the first letter and make the rest lowercase.
    If 'allowed_values' is provided, it will ensure the user input
    is among the allowed values, prompting re-entry if necessary.
    """
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'back':
            raise ExitToMainMenu
        if normalize:
            # Capitalize the first letter and make the rest lowercase
            user_input = user_input.capitalize()
        if allowed_values and user_input not in allowed_values:
            print("Invalid input. Please enter one of the following: "
                  f"{', '.join(allowed_values)}")
            continue  # Prompt the user to re-enter the input
        return user_input


def get_valid_due_date():
    """
    Prompt the user for a due date, validate its format and ensure
    it's a future date. This function repeatedly prompts the user to
    enter a due date in the YYYY-MM-DD format.

    It performs two key validations:
    1. This step confirms the input matches the expected YYYY-MM-DD format.
       If the input does not match the expected format a ValueError is raised,
       and user is informed of the correct format, prompting them to try again.
    2. Compares the input date to today's date to ensure the due date is
       in the future. Dates in the past are not allowed, and the user will
       be asked to provide a new date if the entered date is not in the future.

    The loop continues until a valid future date is provided, ensuring the due
    date is always correctly formatted and suitable for scheduling tasks.
    """
    while True:
        due_date_str = input("Enter Due Date (YYYY-MM-DD): ")
        try:
            # Amended from:geeksforgeeks.org/python-datetime-strptime-function/
            due_date = datetime.datetime.strptime(
                due_date_str, "%Y-%m-%d").date()

            if due_date < datetime.date.today():
                print("The due date must be in the future. Please try again.")
            else:
                return due_date_str  # Return the valid due date string
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


# Define allowed values for task priority and status
# to ensure user inputs are standardized and limited to these options.
priority_allowed_values = ["High", "Medium", "Low"]
status_allowed_values = ["Completed", "Pending"]


# Function to add a row
def add_row_to_sheet():
    """
    Prompts user for task details and adds a new row to the Google Sheet.
    Fields include as listed below Due Date is validated for future
    dates in YYYY-MM-DD format.
    """
    task_id = get_user_input("Enter Task ID: ")
    to_do = get_user_input("Enter task description: ")
    priority = get_user_input(
        "Enter priority (High/Medium/Low): ",
        normalize=True, allowed_values=priority_allowed_values
        )

    # due_date = input("Enter Due Date (YYYY-MM-DD): ")
    due_date = get_valid_due_date()
    status = get_user_input(
        "Enter status (Completed/Pending): ",
        normalize=True, allowed_values=status_allowed_values)

    # Adding the row to the sheet
    row = [task_id, to_do, priority, due_date, status]
    worksheet.append_row(row)
    print("Task added successfully.")


def view_task():
    """
    Prompts the user for a Task ID and displays the details of
    the specified task.
    """
    task_id = input("Enter Task ID to view: ")
    tasks = worksheet.get_all_records()

    # Convert task_id to int for comparison, if necessary
    task_id = int(task_id)

    # Find the task by Task ID
    found_task = next(
        (task for task in tasks if str(task['Task ID']) == str(task_id)), None
    )

    if found_task:
        print(
            "Task Details:\n"
            f"Task ID: {found_task['Task ID']}\n"
            f"To-Do: {found_task['To-Do']}\n"
            f"Priority: {found_task['Priority']}\n"
            f"Due Date: {found_task['Due Date']}\n"
            f"Status: {found_task['Status']}"
        )
    else:
        print("Task not found.")


def list_all_tasks():
    """
    Retrieves and displays all tasks from the worksheet.

    Each task is fetched as a dictionary from the Google Sheet, displaying
    the Task ID, To-Do, Priority, Due Date, and Status for each.
    If no tasks are found, it notifies the user.
    """
    # Fetch all tasks as a list of dictionaries
    tasks = worksheet.get_all_records()

    # Check if there are any tasks to list
    if tasks:
        for task in tasks:
            print(f"Task ID: {task['Task ID']}, To-Do: {task['To-Do']}, "
                  f"Priority: {task['Priority']}, "
                  f"Due Date: {task['Due Date']}, "
                  f"Status: {task['Status']}")
    else:
        print("No tasks found.")


def main_menu():
    """
    Displays the main menu of the Task Organizer application and provides
    access to all program functions. The function loops until the user decides
    to exit by choosing that option.
    Each option triggers the corresponding program function based on the
    user's choice, but only one function is run at a time, depending on the
    user's input. Invalid inputs prompt a reiteration of the menu and the
    request for a valid choice.
    """
    while True:
        try:
            print("\n Menu To-Do-List \n")
            print("1. Add Task")
            print("2. List All Tasks")
            print("3. View Task")
            print("4. Exit \n")
            choice = get_user_input(
                "Enter choice -> (type 'back' to return to this menu): "
            )
            if choice == "1":
                add_row_to_sheet()
            elif choice == "2":
                list_all_tasks()
            elif choice == "3":
                view_task()
            elif choice == "4":
                print("Exiting the Task Organizer. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ExitToMainMenu:
            # If "back" is entered at any input prompt,
            # loop back to the main menu.
            continue


print("\n Welcome to your Task Organizer")
main_menu()
