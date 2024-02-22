import gspread
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
#worksheet = SHEET.worksheet('taskdb')
worksheet = SHEET.worksheet('test-sheet')


# Function to add a row
def add_row_to_sheet():
    task_id = input("Enter Task ID: ")
    task_name = input("Enter Task Name: ")
    priority = input("Enter Priority (High/Medium/Low): ")
    due_date = input("Enter Due Date (YYYY-MM-DD): ")
    status = input("Enter Status (Completed/Pending): ")

    # Adding the row to the sheet
    row = [task_id, task_name, priority, due_date, status]
    worksheet.append_row(row)
    print("Task added successfully.")


def list_all_tasks():
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
    while True:
        print("\n My Task Organizer menu \n")
        print("1. Add Task")
        print("2. List All Tasks")
        print("3. Exit")
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


if __name__ == "__main__":
    main_menu()
