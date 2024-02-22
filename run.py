import datetime # From www.geeksforgeeks.org/python-datetime-module/
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


# Function to add a row
def add_row_to_sheet():
    """
    Prompts user for task details and adds a new row to the Google Sheet.
    Fields include as listed below Due Date is validated for future
    dates in YYYY-MM-DD format.
    """
    task_id = input("Enter Task ID: ")
    task_name = input("Enter Task Name: ")
    priority = input("Enter Priority (High/Medium/Low): ")
    # due_date = input("Enter Due Date (YYYY-MM-DD): ")
    due_date = get_valid_due_date()
    status = input("Enter Status (Completed/Pending): ")

    # Adding the row to the sheet
    row = [task_id, task_name, priority, due_date, status]
    worksheet.append_row(row)
    print("Task added successfully.")


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
    to exit by choosing Option 3.
    Each option triggers the corresponding program function based on the
    user's choice, but only one function is run at a time, depending on the
    user's input. Invalid inputs prompt a reiteration of the menu and the
    request for a valid choice.
    """
    while True:
        print("\n Menu To-Do-List \n")
        print("1. Add Task")
        print("2. List All Tasks")
        print("3. Exit \n")
        choice = input("Enter choice:")

        if choice == "1":
            add_row_to_sheet()
        elif choice == "2":
            list_all_tasks()
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")


print("\n Welcome to your Task Organizer")
main_menu()


