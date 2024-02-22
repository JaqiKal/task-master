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
worksheet = SHEET.worksheet('test-sheet')


# Function to add a row
def add_row_to_sheet():
    task_id = input("Enter Task ID: ")
    task_name = input("Enter Task Name: ")
    priority = input("Enter Priority (High/Medium/Low): ")
    due_date = input("Enter Due Date (YYYY-MM-DD): ")
    status = input("Enter Status (Completed/Pending): ")

    # Adding the row to the worksheet
    row = [task_id, task_name, priority, due_date, status]
    worksheet.append_row(row)
    print("Task added successfully.")


# Calling the function
add_row_to_sheet()
