# Amended from www.geeksforgeeks.org/python-datetime-module/
import datetime
# Amended from Code Institute project love_sandwiches
import gspread
from google.oauth2.service_account import Credentials
# Amended from pypi.org/project/prettytable/
from prettytable import PrettyTable

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Google Sheets setup
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("task-master-database")
# Attempt to open the worksheet
try:
    worksheet = SHEET.worksheet("test-sheet")
    # If the worksheet is found, continue with the program
except gspread.WorksheetNotFound:
    # If the worksheet is not found, print an error message and exit
    # API error handling amended from docs.gspread.org/en/latest/api/exceptions.html
    # and  snyk.io/advisor/python/gspread/functions/gspread.exceptions.APIError
    print("Error: Worksheet not found")
    exit()


class ExitToMainMenu(Exception):
    """
    Amended from: stackoverflow.com/questions/1319615/
    proper-way-to-declare-custom-exceptions-in-modern-python

    Exception used to signal an exit back to the main menu.
    """

    pass


def generate_task_id():
    """
    Generates a unique, sequential task ID for new tasks.
    This function fetches all current tasks from the Google Sheet,
    identifies the highest task ID in use, and increments it by 1 to
    ensure uniqueness and maintain a sequential order.
    The ethod is chosen for its simplicity and effectiveness in environments
    where task creation occurs at a manageable rate and concurrency issues
    are minimal. It leverages the existing data structure without requiring
    external dependencies or complex ID generation schemes.
    """
    # Fetch all tasks as a list of dictionaries
    tasks = worksheet.get_all_records()

    # If there are no tasks, start with ID 1
    if not tasks:
        return 1

    # Extract Task IDs and convert them to integers
    task_ids = [int(task["Task ID"]) for task in tasks]

    # Find the highest task ID and add 1 to generate the next ID
    next_id = max(task_ids) + 1 if task_ids else 1

    return next_id


def get_user_input(
    prompt,
    normalize=False,
    allowed_values=None,
    allow_skip=False
):
    """
    Amended from: www.geeksforgeeks.org/string-capitalize-python/
    Inspo on removing leading or trailing whitespace characters is
    found at: www.codeease.net/programming/python/python-input-strip

    Prompts the user for input and allows exit to the main menu
    upon receiving a specific input. If 'normalize' is True,
    it will capitalize the first letter and make the rest lowercase.
    If 'allowed_values' is provided, it will ensure the user input
    is among the allowed values, prompting re-entry if necessary.
    Function also reject empty inputs with consistent error feedback,
    but enables skipping an action with empty input if 'allow_skip'
    is set to True.
    """
    while True:
        # Stripping leading/trailing whitespace
        user_input = input(prompt).strip()
        if user_input.lower() == "back":
            raise ExitToMainMenu
        # Return empty input to signify skipping
        if allow_skip and user_input == "":
            return user_input
        # Check for empty input
        if not user_input:
            print("Input cannot be empty. Please try again.\n")
            continue
        # Capitalize the first letter and make the rest lowercase
        if normalize:
            user_input = user_input.capitalize()
        # Prompt the user to re-enter the input
        if allowed_values and user_input not in allowed_values:
            print(
                "Invalid input. Please enter one of the following:\n"
                f"{', '.join(allowed_values)}"
            )
            continue
        return user_input


def get_valid_due_date():
    """
    Prompt the user for a due date, validate its format and ensure
    it's a future date. This function repeatedly prompts the user to
    enter a due date in the YYYY-MM-DD format.

    It performs two key validations:
    1. This step confirms the input matches the expected YYYY-MM-DD
       format. If the input does not match the expected format a
       ValueError is raised, and user is informed of the correct format,
       prompting them to try again
    2. Compares the input date to today's date to ensure the due date
       is in the future. Dates in the past are not allowed, and the user
       will be asked to provide a new date if the entered date is not in
       the future.

    The loop continues until a valid future date is provided, ensuring
    the due date is always correctly formatted and suitable for scheduling
    tasks.
    """
    while True:
        due_date_str = input("Enter Due Date (YYYY-MM-DD): \n")
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
status_allowed_values = ["New", "Completed", "Pending"]


# Function to add a row
def add_row_to_sheet():
    """
    Prompts user for task details and adds a new row to the Google Sheet.
    Fields include as listed below Due Date is validated for future
    dates in YYYY-MM-DD format.
    """
    # Generate & display the Task ID
    task_id = generate_task_id()
    print(f"Task ID: {task_id}")
    # User adds task description
    to_do = get_user_input("Enter task description: \n")
    # User adds priority
    priority = get_user_input(
        "Enter priority (High/Medium/Low): \n",
        normalize=True,
        allowed_values=priority_allowed_values,
    )
    # User adds due_date = input("Enter Due Date (YYYY-MM-DD): ")
    due_date = get_valid_due_date()
    # User adds status
    status = get_user_input(
        "Enter status (New/Completed/Pending): \n",
        normalize=True,
        allowed_values=status_allowed_values,
    )
    # Generate the task creation date in YYYY-MM-DD format
    creation_date = datetime.date.today().strftime("%Y-%m-%d")

    # Adding the row to the sheet with API error handling
    # Amended from docs.gspread.org/en/latest/api/exceptions.html
    # and  snyk.io/advisor/python/gspread/functions/gspread.exceptions.APIError
    row = [task_id, to_do, priority, due_date, status, creation_date]
    try:
        worksheet.append_row(row)
        print("\nTask added successfully with creation date:", creation_date)
    except gspread.exceptions.APIError as e:
        # Print API error
        print("Failed to add task due to Google sheets API error:", e)

def list_all_tasks():
    """
    Amended from pypi.org/project/prettytable/

    Retrieves and displays all tasks from the worksheet in a formatted table.
    Each task is fetched as a dictionary from the Google Sheet, displaying
    the Task ID, To-Do, Priority, Due Date, Status and Creation Date for
    each in a visually appealing table format. If no tasks are found,
    it notifies the user.
    """
    # Fetch all tasks as a list of dictionaries
    tasks = worksheet.get_all_records()

    # Create a PrettyTable instance and define the column headers
    table = PrettyTable()
    table.field_names = [
        "Task ID",
        "To-Do",
        "Priority",
        "Due Date",
        "Status",
        "Creation Date",
    ]
    table.align = "l"

    # Iterate over all tasks and add them to the table
    for task in tasks:
        table.add_row(
            [
                task["Task ID"],
                task["To-Do"],
                task["Priority"],
                task["Due Date"],
                task["Status"],
                task["Creation Date"],
            ]
        )

    # Check if there are any tasks to list
    if tasks:
        print(table)
    else:
        print("No tasks found.")


def view_task():
    """
    Prompts the user for a Task ID and displays the details of
    the specified task.
    """
    task_id = input("Enter Task ID to view: \n")
    tasks = worksheet.get_all_records()

    # Find the task by Task ID
    found_task = next(
        (task for task in tasks if str(task["Task ID"]) == str(task_id)), None)

    if found_task:
        # Create a PrettyTable instance and define the column headers
        task_table = PrettyTable()
        task_table.field_names = [
            "Task ID",
            "To-Do",
            "Priority",
            "Due Date",
            "Status",
            "Creation Date"
            ]
        task_table.align = "l"

        # Add the found task to the table
        task_table.add_row([
            found_task["Task ID"],
            found_task["To-Do"],
            found_task["Priority"],
            found_task["Due Date"],
            found_task["Status"],
            found_task["Creation Date"]
        ])

        # Print the task details table
        print(task_table)
    else:
        print("Task not found.")


def view_task_specific(task_id):
    """
    Displays the details of a specific task identified by its Task ID.
    This function fetches the task's details from the Google Sheet
    and prints them.
    """
    # Fetch all tasks as a list of dictionaries
    tasks = worksheet.get_all_records()

    # Find the task by Task ID
    found_task = next(
        (
            task for task in tasks
            if str(task["Task ID"]) == task_id
        ),
        None
    )

    # If the task is found, display its details
    if found_task:
        print(f"Task ID: {found_task['Task ID']}")
        print(f"To-Do: {found_task['To-Do']}")
        print(f"Priority: {found_task['Priority']}")
        print(f"Due Date: {found_task['Due Date']}")
        print(f"Status: {found_task['Status']}")
        print(f"Creation Date: {found_task['Creation Date']}")
    else:
        print("Task not found.")


def update_task():
    """
    This function allows user to update an exisiting task in the task
    organizer. Unlike other functions that require user input for every field,
    this function allows optional updates:
    - Empty input for any field (except the Task ID) skips the update for
      that field, leaving the original value unchanged.
    - The function validates the Task ID and informs the user if the specified
      task cannot be found.
    - For the due date, the function checks for valid date format (YYYY-MM-DD)
      and skips update if the format is incorrect, without terminating the
      update process.
    - checks to notify the user if the new priority or status is the same
      as the current one, avoiding unnecessary updates.
    - Utilizes the `ExitToMainMenu` exception to allow exiting to the main menu
      at any point by typing a specific command (e.g., 'back')
    """
    try:
        task_id = get_user_input(
            "Enter the Task ID of the task you want to update: \n",
            normalize=False
        )

        tasks = worksheet.get_all_records()
        task_index = None

        # Iterates through tasks to find the index of the task with
        # the specified Task ID.
        for index, task in enumerate(tasks):
            if str(task["Task ID"]) == task_id:
                # Considering header row and 1-based indexing
                task_index = index + 2
                # Assign the task details to current_task
                current_task = task
                break

        if current_task is None:
            print(
                "Task not found." "Please ensure you have entered the"
                "correct Task ID."
            )
            return

        print("\nCurrent task details:")
        print("---------------------")
        view_task_specific(task_id)

        # Ask the user for a new description, stripping
        # leading/trailing whitespace
        new_description = get_user_input(
            "\nEnter new description (or press Enter to skip): \n",
            normalize=False,
            allowed_values=None,
            allow_skip=True,
        ).strip()

        # If the user entered a new description, update the task's
        # description in the sheet
        if new_description:
            worksheet.update_cell(task_index, 2, new_description)

        # Prompt for a new priority, allowing an empty input to skip
        # the update
        new_priority = get_user_input(
            "Enter new priority (High/Medium/Low) or press Enter to skip: ",
            normalize=True,
            allowed_values=priority_allowed_values + [""],
            allow_skip=True,
        )

        # Notify the user if the new priority is the same as the current one.
        if new_priority and new_priority.lower(
            ) == current_task["Priority"].lower():
            confirm_change = input(
                "The new priority is the same as the current one."
                "Do you still want to change it? (yes/no): \n").strip().lower()
            if confirm_change == "yes":
                worksheet.update_cell(task_index, 3, new_priority)
            else:
                print("Priority update skipped.")
            # If a new priority is provided, update it in the sheet
        elif new_priority:
            worksheet.update_cell(task_index, 3, new_priority)

        # Handle invalid date formats gracefully
        # ask for a new due date, allowing an empty input to skip
        new_due_date = get_user_input(
            "\nEnter new Due Date (YYYY-MM-DD) or press Enter to skip: \n",
            allow_skip=True)
        if new_due_date:
            try:
                # Validate the date format by attempting to convert
                # the string into a date
                due_date = datetime.datetime.strptime(
                    new_due_date, "%Y-%m-%d").date()
                if due_date < datetime.date.today():
                    print("Due date must be in the future. Please try again.")
                else:
                    worksheet.update_cell(task_index, 4, new_due_date)
            except ValueError:
                # If the date format is invalid, inform user
                # and skip updating the due date
                print("Invalid date format. Skipped updating due date.\n")

        # Ask the user for a new status, allowing an empty input
        # to skip the update
        new_status = get_user_input(
            "Enter new status (New/Completed/Pending) or press"
            "Enter to skip: \n",
            normalize=True,
            allowed_values=status_allowed_values + [""],
            allow_skip=True,
        )

        # Notify the user if the new status is the same as the current one.
        if new_status and new_status.lower() == current_task["Status"].lower():
            # Ask the user if they want to proceed with changing the status
            # even though it's the same as the current one
            confirm_change_status = input(
                "The new status is the same as the current one."
                " Do you still want to change it? (yes/no): ").strip().lower()
            if confirm_change_status == "yes":
                # If the user confirms, proceed with updating the status
                worksheet.update_cell(task_index, 5, new_status)
                print("Status updated successfully.")
            else:
                # If the user decides not to change the status, skip this part
                print("Status update skipped.")
        elif new_status:
            # If the new status is different from the current one, update it
            worksheet.update_cell(task_index, 5, new_status)
        print("Task updated successfully.")
    except ExitToMainMenu:
        return


def delete_tasks():
    """
    Allows the user to delete a task from the task organizer.
    The function prompts the user for the Task ID of the task they
    wish to delete. It checks if the task exists, and if so,
    deletes it from the Google Sheet. If the task cannot be found,
    user is informed accordingly.

    Allows the user to delete multiple tasks from the task organizer.
    The function prompts the user for the Task IDs of the tasks they
    wish to delete, separated by commas. It checks if each task exists,
    and if so, deletes it from the Google Sheet. If any task cannot be found,
    the user is informed accordingly.
    """
    try:
        task_ids_input = get_user_input(
            "Enter the Task ID(s) of the tasks you want to delete"
            "(separated by commas): \n",
            normalize=False,
        )
        # Split the input into a list of task IDs, trimming whitespace
        task_ids = [task_id.strip() for task_id in task_ids_input.split(",")]

        tasks = worksheet.get_all_records()
        tasks_to_delete = []

        # Collect rows (indexes) to delete
        for task_id in task_ids:
            for index, task in enumerate(tasks):
                if str(task["Task ID"]) == task_id:
                    # Considering header row and 1-based indexing
                    tasks_to_delete.append(index + 2)

        if not tasks_to_delete:
            print(
                "None of the specified Task IDs were found."
                " Please ensure you have entered the correct Task IDs."
            )
            return

        # Confirm deletion with the user before proceeding
        confirm = (
            input(
                "Are you sure you want to delete these tasks?"
                " The action is irreversible! (yes/no): "
            )
            .strip()
            .lower()
        )

        if confirm == "yes":
            # Sort the list in reverse order to avoid messing up the indexes
            tasks_to_delete.sort(reverse=True)
            try:
                for row in tasks_to_delete:
                    worksheet.delete_rows(row)
                    print("Tasks deleted successfully.")
            except gspread.exceptions.APIError as e:
                # Print the API error
                print("Failed to delete task due to a GOoogle sheet API error:", e)
        elif confirm == "no":
            print("Task deletion canceled.")
        else:
            print("Invalid input. Please answer 'yes' or 'no'.")

    except ExitToMainMenu:
        return


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
            print("\n Menu To-Do-List")
            print("-----------------")
            print("1. Add Task")
            print("2. List All Tasks")
            print("3. View Task")
            print("4. Update Task")
            print("5. Delete Task(s)")
            print("6. Exit application\n")
            choice = get_user_input(
                "Enter choice -> (or type 'back' to return to menu): \n"
            )
            # Adds a blank line for clearer output separation
            print()
            if choice == "1":
                add_row_to_sheet()
            elif choice == "2":
                list_all_tasks()
            elif choice == "3":
                view_task()
            elif choice == "4":
                update_task()
            elif choice == "5":
                delete_tasks()
            elif choice == "6":
                print("Exiting the Task Organizer. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ExitToMainMenu:
            # If "back" is entered at any input prompt,
            # loop back to the main menu
            continue


print(
    "\nWelcome to Your Personal Task Organizer! 🌟 \n"
    "Effortlessly manage your tasks with our intuitive task organizer."
    "\nStay organized, focused, and productive by easily adding, updating,"
    "\nand tracking your to-dos."
    "\nGet started now and make task management a breeze!\n"
)

main_menu()
