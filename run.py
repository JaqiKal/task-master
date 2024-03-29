"""
This is the main and only script for the Task Master application, a tool
designed to simplify task management. The application allows users to add,
manage, and track tasks with ease. It leverages the power of Google Sheets for
data storage, ensuring that your task list is accessible and up-to-date. It
features a menu-driven interface for straightforward navigation and is built to
support a wide range of task management activities, from setting due dates to
prioritizing tasks.

By: JaqiKal
Date: March 2024
"""

# Amended from: www.geeksforgeeks.org/clear-screen-python/
import os
# Amended from: www.geeksforgeeks.org/python-datetime-module/
import datetime
# Amended from: Code Institute project love_sandwiches
import gspread
from google.oauth2.service_account import Credentials
# Amended from: pypi.org/project/prettytable/
from prettytable import PrettyTable
# Amended from: www.geeksforgeeks.org/print-colors-python-terminal/
import colorama
from colorama import Fore, Style
# Amended from: docs.gspread.org/en/latest/api/exceptions.html
from gspread.exceptions import APIError

# Initialize colorama
colorama.init()

# Amended from: Code Institute project love_sandwiches
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

# Google Sheets setup
# Amended from: Code Institute project love_sandwiches
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("task-master-database")

# Attempt to open the worksheet
# Amended from: www.w3schools.com/python/python_try_except.asp
try:
    worksheet = SHEET.worksheet("taskdb")
    # If the worksheet is found, continue with the program
except gspread.WorksheetNotFound:
    # If the worksheet is not found, print an error message and exit
    # API error handling amended from:
    # docs.gspread.org/en/latest/api/exceptions.html
    # and  snyk.io/advisor/python/gspread/functions/gspread.exceptions.APIError
    print(
            f"{Fore.RED}{Style.BRIGHT}Error: Worksheet not found."
            f"Please check the worksheet name and try again.{Style.RESET_ALL}"
        )
    exit()


# Define allowed values for task priority and status
# to ensure user inputs are standardized and limited to these options.
priority_allowed_values = ["High", "Med", "Low"]
status_allowed_values = ["New", "Done", "Pend"]


class ExitToMainMenu(Exception):
    """
    Amended from: stackoverflow.com/questions/1319615/
    proper-way-to-declare-custom-exceptions-in-modern-python
    Exception used to signal an exit back to the main menu.
    """


def generate_task_id():
    """
    Generates a unique, sequential task ID for new tasks. This function fetches
    all current tasks from the Google Sheet, identifies the highest task ID in
    use, and increments it by 1 to ensure uniqueness and maintain a sequential
    order. The method is chosen for its simplicity and effectiveness in
    environments where task creation occurs at a manageable rate and
    concurrency issues are minimal. It leverages the existing data structure
    without requiring external dependencies or complex ID generation schemes.
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
    allow_skip=False,
    numeric=False
):
    """
    Amended from: www.geeksforgeeks.org/string-capitalize-python/
    Inspo on removing leading or trailing whitespace characters is
    found at: www.codeease.net/programming/python/python-input-strip

    Prompts the user for input and allows exit to the main menu upon receiving
    a specific input. If 'normalize' is True, it will capitalize the first
    letter and make the rest lowercase. If 'allowed_values' is provided, it
    will ensure the user input is among the allowed values, prompting re-entry
    if necessary. Function also reject empty inputs with consistent error
    feedback, but enables skipping an action with empty input if 'allow_skip'
    is set to True.
    """
    while True:
        # Colorize and reset prompt color within the function
        user_input = input(
            Fore.LIGHTBLUE_EX + Style.BRIGHT + prompt + Fore.RESET
        ).strip()

        # Handle 'back' to exit or 'skip' functionality
        if user_input.lower() == "back":
            raise ExitToMainMenu

        # Return empty input to signify skipping
        if allow_skip and user_input == "":
            return user_input
        # Check for empty input
        if not user_input:
            print(
                f"{Fore.RED}{Style.BRIGHT}Error: Input cannot be empty.\n"
                f"Please try again.{Style.RESET_ALL}\n"
            )
            continue

        # Capitalize the first letter and make the rest lowercase
        if normalize:
            user_input = user_input.capitalize()
        # Prompt the user to re-enter the input
        if allowed_values and user_input not in allowed_values:
            print(f"{Fore.RED}{Style.BRIGHT}"
                  "Error: Invalid input.\n"
                  "Please enter one of the following: "
                  f"{', '.join(allowed_values)}{Style.RESET_ALL}\n"
                  )
            continue

        # Attempt to convert input to integer, retrying on failure
        if numeric:
            # Amended from: www.w3schools.com/python/python_try_except.asp
            try:
                # Convert to integer and return if successful
                return int(user_input)
            except ValueError:
                print(
                     f"{Fore.RED}{Style.BRIGHT}Error: Invalid input.\n"
                     "Please enter a numeric value.\n"
                     f"{Style.RESET_ALL}"
                )
            continue
        # Ensure a newline for readability
        print()
        return user_input


def get_valid_due_date():
    """
    Prompt the user for a due date, validate its format and ensure
    it's a future date. This function repeatedly prompts the user to
    enter a due date in the YY-MM-DD format.

    It performs two key validations:
    1. This step confirms the input matches the expected YY-MM-DD
    2. Compares the input date to today's date to ensure the due date
       is in the future.
    The loop continues until a valid future date is provided, ensuring
    the due date is always correctly formatted and suitable for scheduling
    tasks.
    """
    while True:
        due_date_str = input(
            f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}"
            "Enter Due Date (YY-MM-DD): \n"
            f"{Style.RESET_ALL}")

        # Check for 'back' command to return or exit
        if due_date_str.lower() == "back":
            raise ExitToMainMenu

        # Check for empty input
        if not due_date_str:
            print(
                f"{Fore.RED}{Style.BRIGHT}"
                "Error: Input cannot be empty.\n"
                "Please try again."
                f"{Style.RESET_ALL}\n")
            continue

        # Split the input string by '-' and check if year, month, and day
        # components are of the expected length
        parts = due_date_str.split("-")
        if (len(parts) == 3 and
           len(parts[0]) == 2 and
           len(parts[1]) == 2 and
           len(parts[2]) == 2):
            # Amended from: www.w3schools.com/python/python_try_except.asp
            try:
                # Amended from:
                # geeksforgeeks.org/python-datetime-strptime-function/
                due_date = datetime.datetime.strptime(
                    due_date_str, "%y-%m-%d"
                ).date()

                if due_date < datetime.date.today():
                    print(
                        f"{Fore.RED}{Style.BRIGHT}"
                        "Error: The due date must be in the future.\n"
                        "Please try again."
                        f"{Style.RESET_ALL}\n"
                    )
                else:
                    # Return the valid due date string
                    return due_date_str
            except ValueError:
                print(
                    f"{Fore.RED}{Style.BRIGHT}"
                    "Error: Invalid date format.\n"
                    "Please use YY-MM-DD."
                    f"{Style.RESET_ALL}\n"
                    )
        else:
            # If the input does not match the expected component lengths
            print(
                f"{Fore.RED}{Style.BRIGHT}"
                "Error: Date format must be YY-MM-DD with\n"
                "two digits for year, month, and day.\n"
                "Please try again."
                f"{Style.RESET_ALL}\n"
            )


def add_row_to_sheet():
    """
    Prompts user for task details and adds a new row to the Google Sheet.
    Fields include as listed below Due Date is validated for future
    dates in YY-MM-DD format.
    """
    # Generate & display the Task ID
    task_id = generate_task_id()
    print(
        f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}"
        "Task ID generated automatically:\n"
        f"{Style.RESET_ALL}"
        f"Task ID: {task_id}\n"
        )
    # User adds task description
    to_do = get_user_input("Enter task description: \n")

    # User adds priority
    priority = get_user_input(
        "Enter priority (High/Med/Low): \n",
        normalize=True,
        allowed_values=priority_allowed_values,
    )

    # User adds due date = input("Enter Due Date (YY-MM-DD): ")
    due_date = get_valid_due_date()
    # Readibility
    print()

    # User adds status
    status = get_user_input(
        "Enter status (New/Done/Pend): \n",
        normalize=True,
        allowed_values=status_allowed_values,
    )

    # Generate the task creation date in YY-MM-DD format
    creation_date = datetime.date.today().strftime("%y-%m-%d")

    # Adding the row to the sheet with API error handling
    # Amended from docs.gspread.org/en/latest/api/exceptions.html
    # and  snyk.io/advisor/python/gspread/functions/gspread.exceptions.APIError
    row = [task_id, to_do, priority, due_date, status, creation_date]
    # Amended from: www.w3schools.com/python/python_try_except.asp
    try:
        worksheet.append_row(row)
        print(f"{Fore.GREEN}{Style.BRIGHT}"
              "Task added successfully with creation date: "
              f"{creation_date}{Style.RESET_ALL}")

    # print("\nTask added successfully with creation date:", creation_date)
    except gspread.exceptions.APIError as e:
        # Print API error
        print(f"{Fore.RED}{Style.BRIGHT}"
              "Error: Failed to add task due to Google sheets API error: "
              f"{e}{Style.RESET_ALL}\n")


def wrap_text(text, width):
    """
    Function handles text wrapping for displaying task descriptions
    within Table output. Initially attempted using 'textwrap' lib to
    manage overflow, but content still exceeded boundaries. This prioritizes
    keeping text intact or breaking at spaces, resorting to hard breaks when
    necessary. Not ideal for maintaining readability for long text that should
    be kept intact or broken wih hyphens, but for this app purpose it works.
    This function has been modified to strip leading and trailing spaces
    from the input text before wrapping. It checks if the stripped text is
    empty and returns an empty list if so, ensuring that long empty strings
    are handled more gracefully. It maintains readability for this app's
    context, ensuring descriptions fit within specified width constraints
    without awkward word splits, and with improved handling of long empty
    strings.
    """
    # Ensure all inputs are treated as strings
    # and strip leading/trailing spaces
    text = str(text).strip()
    # Check if the string is empty after stripping
    if not text:
        # Return a list with an empty string if the text is empty
        return ['']
    if len(text) <= width:
        # Return the text if it's short enough
        return [text]

    wrapped_text = []
    while text:
        if len(text) <= width:
            wrapped_text.append(text)
            break
        else:
            # Find space to break the line, if possible
            space_index = text.rfind(' ', 0, width)
            if space_index != -1:
                # Break line at last space within width
                wrapped_text.append(text[:space_index])
                # Skip the space
                text = text[space_index+1:]
            else:
                # No space found; hard break at the width limit
                wrapped_text.append(text[:width])
                text = text[width:]
    return wrapped_text


def list_all_tasks():
    """
    Retrieves and displays all tasks from the worksheet in a formatted table.
    It offers sorting based on user preference for priority, status, or
    due_date, with a default sorting by Task ID.

    This function incorporates sorting functionality, with modifications
    and adaptations based on examples from the following sources:
    - ioflood.com/blog/python-sort-dictionary-by-value/#:~:
    text=TL%3BDR%3A%20How%20Do%20I,items()%2C%20key%3Doperator.
    - /pythonhow.com/how/sort-a-list-of-dictionaries-by-a-value-
    of-the-dictionary/
    - www.geeksforgeeks.org/ways-sort-list-dictionaries-values-
    python-using-lambda-function/
    """
    tasks = worksheet.get_all_records()

    if not tasks:
        print(f"{Fore.RED}{Style.BRIGHT}"
              "No tasks found."
              f"{Style.RESET_ALL}"
              )
        return

    # Ask the user for their preferred sorting criteria
    print("Sort Task By")
    print("------------")
    # Print the options with the selected header color
    print("1. Task ID (default)")
    print("2. Priority (High to Low)")
    print("3. Status (New to Done)")
    print("4. Due Date (earliest to latest)")
    print("5. Due Date (latest to earliest)")
    print("6. Back to Main Menu")

    # Amended from: www.w3schools.com/python/python_try_except.asp
    try:

        # Get user input for sorting choice
        sort_choice = get_user_input(
            "\nPlease, select an option (1-6) or press Enter for default: \n",
            allow_skip=True, numeric=True
        )

        # Default to sorting by Task ID if no valid choice is made
        # and ensure the sort_choice is correctly interpreted as an integer
        sort_choice = int(sort_choice) if sort_choice else 1

        if sort_choice is None or sort_choice == 6:
            print(
                f"{Fore.GREEN}{Style.BRIGHT}"
                "\nYou have returned to main menu."
                "\nFeel free to explore more options!"
                f"{Style.RESET_ALL}"
                )
            return

        # Define custom sort orders for priority and status
        priority_order = {"High": 1, "Med": 2, "Low": 3}
        status_order = {"New": 1, "Pend": 2, "Done": 3}

        # Define the sorting key7
        def sort_key(x):
            if sort_choice == 2:
                return priority_order.get(x["Priority"], 999)
            elif sort_choice == 3:
                return status_order.get(x["Status"], 999)
            elif sort_choice in [4, 5]:
                # Convert string to datetime.date for proper comparison
                return datetime.datetime.strptime(
                    x["Due Date"], "%y-%m-%d").date(
                    )
            # Default to sorting by Task ID
            else:
                return int(x["Task ID"])

        # Determine if sorting should be reversed based on user choice
        reverse_sort = sort_choice == 5
        # Perform the sorting
        sorted_tasks = sorted(tasks, key=sort_key, reverse=reverse_sort)

    except ExitToMainMenu:
        # If 'back' is entered, catch the exception and return immediately
        return
    except KeyError as e:
        print(
            f"{Fore.RED}{Style.BRIGHT}"
            f"An error occurred due to a missing key during sorting: {e}."
            f"{Style.RESET_ALL}"
            )
        sorted_tasks = sorted(tasks, key=lambda x: int(x["Task ID"]))
    except ValueError as e:
        print(
            f"{Fore.RED}{Style.BRIGHT}"
            f"An error occurred due to a value problem during sorting: {e}."
            f"{Style.RESET_ALL}"
            )
        sorted_tasks = sorted(tasks, key=lambda x: int(x["Task ID"]))
    except Exception as e:
        print(
            f"{Fore.RED}{Style.BRIGHT}"
            f"An unexpected error occurred during sorting: {e}."
            " Proceeding with caution."
            f"{Style.RESET_ALL}"
            )
        sorted_tasks = sorted(tasks, key=lambda x: int(x["Task ID"]))

    # Adding a space before displaying the table for better readability
    print()

    # Prepare and display the table
    table = PrettyTable()
    table.field_names = [
        "ID",
        "To-Do",
        "Prio",
        "Due Date",
        "Status",
        "Created ",
    ]
    table.align = "l"

    # Max width for the To-Do column
    max_width = 30

    for task in sorted_tasks:
        wrapped_text = wrap_text(task["To-Do"], max_width)

        # The first row with all the task details
        first_line = [
                task["Task ID"],
                wrapped_text[0],
                task["Priority"],
                task["Due Date"],
                task["Status"],
                task["Creation Date"],
            ]
        table.add_row(first_line)

        # For the additional lines from the wrapped text, add empty
        # placeholders for all columns except the "To-Do" column
        # which gets the additional text
        for line in wrapped_text[1:]:
            # Create a row with empty values for all but the "To-Do" column
            # Empty placeholders for other columns
            additional_line = [""] * (len(table.field_names))
            # Insert the wrapped text line into the correct position
            # for "To-Do"
            additional_line[1] = line
            table.add_row(additional_line)

    # Print the task details table with colored text
    print(
        Fore.LIGHTBLUE_EX + Style.BRIGHT + str(table) + Fore.RESET
        )


def view_task():
    """
    Prompts the user for a Task ID and displays the details of
    the specified task.
    """
    task_id = get_user_input(
        "Enter Task ID to view (type 'back' for Main Menu): \n",
        numeric=True)
    tasks = worksheet.get_all_records()

    # Find the task by Task ID
    found_task = next(
        (task for task in tasks if int(task["Task ID"]) == task_id),
        None)

    if found_task:
        # Code to display the task details. Create a PrettyTable
        # instance and define the column headers
        task_table = PrettyTable()
        task_table.field_names = [
            "ID",
            "To-Do",
            "Prio",
            "Due Date",
            "Status",
            "Created",
        ]

        task_table.align = "l"

        # Max width for the To-Do column
        max_width = 30
        wrapped_text = wrap_text(found_task["To-Do"], max_width)

        # Add the found task to the table
        first_line = [
            found_task["Task ID"],
            wrapped_text[0] if wrapped_text else "",
            found_task["Priority"],
            found_task["Due Date"],
            found_task["Status"],
            found_task["Creation Date"],
        ]
        task_table.add_row(first_line)

        # If 'To-Do' text was wrapped to more lines, add them to the table
        for line in wrapped_text[1:]:
            task_table.add_row(["", line, "", "", "", ""])

        # For readability
        print()

        # Print the task details table with colored text
        print(
            Fore.BLUE + Style.BRIGHT + str(task_table) + Fore.RESET
            )

    else:
        # No task was found with the given Task ID
        print(f"{Fore.RED}{Style.BRIGHT}"
              "\nError: Task not found.\n"
              "Please ensure you have entered a valid Task ID."
              "\nYou have returned to main menu."
              f"{Style.RESET_ALL}\n"
              )


def update_task():
    """
    This function allows user to update an exisiting task in the task
    organizer. Unlike other functions that require user input for every field,
    this function allows optional updates:
    """
    # Amended from: www.w3schools.com/python/python_try_except.asp
    current_task = None

    try:
        task_id = get_user_input(
            "Enter the Task ID of the task you want to update: \n",
            normalize=False
        )
        tasks = worksheet.get_all_records()
        # Initialize current_task to None before the loop
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
            print(f"{Fore.RED}{Style.BRIGHT}"
                  "Error: Task not found. \n"
                  "Please ensure you have entered the correct Task ID.\n"
                  "Check with the help of Main Menu item no. 2"
                  f"{Style.RESET_ALL}")
            return

        print("Update Task Details (or type 'back' for Main Menu):")
        print("---------------------------------------------------")

        # Ask the user for a new description, stripping
        # leading/trailing whitespace
        new_description = get_user_input(
            "Please, enter new description, or press Enter to skip: \n",
            normalize=False,
            allowed_values=None,
            allow_skip=True,
        ).strip()

        # If the user entered a new description, update the task's
        # description in the sheet
        if new_description:
            worksheet.update_cell(task_index, 2, new_description)
            print(
                f"{Fore.GREEN}{Style.BRIGHT}"
                "Description updated successfully.\n"
                f"{Style.RESET_ALL}")

        # Prompt for a new priority, allowing an empty input to skip
        # the update
        while True:
            new_priority = get_user_input(
                "Enter new priority (High/Med/Low) "
                "or press Enter to skip: \n",
                normalize=True,
                allowed_values=["High", "Med", "Low", ""],
                allow_skip=True
                )

            if new_priority == "":
                break

            if new_priority.lower() == current_task["Priority"].lower():
                print(
                    f"{Fore.YELLOW}{Style.BRIGHT}"
                    "The new priority is the same as the current one.\n"
                    f"{Fore.GREEN}"
                    "Priority remains unchanged."
                    f"{Style.RESET_ALL}"
                )
                print(
                    f"{Fore.YELLOW}{Style.BRIGHT}"
                    "\nOptions:\n"
                    "- Type 'back' to modify your input.\n"
                    "- Press Enter or any other key to proceed "
                    "without changes.\n"
                    "\nChoose an option:"
                    f"{Style.RESET_ALL}"
                )
                # Using `input` directly for local control
                choice = input().strip().lower()
                if choice == 'back':
                    # Loop back for re-entry
                    continue
                else:
                    # If the user decides not to type 'back',
                    # just proceed without repeating the message.
                    break
            else:
                worksheet.update_cell(task_index, 3, new_priority)
                print(
                    f"{Fore.GREEN}{Style.BRIGHT}"
                    "Priority change successful.\n"
                    f"{Style.RESET_ALL}"
                    )
                break
        # Handle invalid date formats gracefully
        # ask for a new due date, allowing an empty input to skip
        print(
            f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}"
            "Please, enter new Due Date (YY-MM-DD)"
            "or press Enter to skip:"
            f"{Style.RESET_ALL}"
            )
        while True:
            # Directly use input for user interaction
            new_due_date = input().strip()

            # Check for 'back' input to return to the main menu
            if new_due_date.lower() == 'back':
                raise ExitToMainMenu
            # Allow skipping the due date update
            if new_due_date == '':
                break

            try:
                # Amended from: www.w3schools.com/python/python_try_except.asp
                # Validate the date format by attempting to convert
                # the string into a date
                due_date = datetime.datetime.strptime(
                    new_due_date, "%y-%m-%d").date()
                if due_date < datetime.date.today():
                    print(
                        f"{Fore.RED}{Style.BRIGHT}"
                        "\nError: The due date must be in the future.\n"
                        f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}"
                        "\nPlease try again or press Enter to skip.\n"
                        f"{Style.RESET_ALL}"
                        )
                else:
                    # If the date is valid and in the future,
                    # update the due date in the worksheet
                    worksheet.update_cell(task_index, 4, new_due_date)
                    print(
                        f"{Fore.GREEN}{Style.BRIGHT}"
                        "Due date updated successfully."
                        f"{Style.RESET_ALL}\n")
                    # Exit the loop after successful update
                    break
            except ValueError:
                # If the date format is invalid, inform user to try again
                print(
                    f"{Fore.RED}{Style.BRIGHT}"
                    "\nError: Invalid date format.\n"
                    f"{Fore.LIGHTBLUE_EX}{Style.BRIGHT}"
                    "\nPlease use YY-MM-DD or press Enter to skip.\n"
                    f"{Style.RESET_ALL}"
                    )

        # Prompt the user for a new status, allowing an empty input
        # to skip the update
        while True:
            new_status = get_user_input(
                "Please, enter new status (New/Done/Pend) or "
                "press Enter to skip: \n",
                normalize=True,
                allowed_values=["New", "Done", "Pend", ""],
                allow_skip=True,
            )
            if new_status == "":
                print(
                    f"{Fore.GREEN}{Style.BRIGHT}"
                    "Status update skipped."
                    f"{Style.RESET_ALL}"
                    )
                break

            # Notify the user if the new status is the same as the current one.
            if new_status.lower() == current_task["Status"].lower():
                # Ask the user if they want to proceed with changing the status
                # even though it's the same as the current one
                print(
                    f"{Fore.YELLOW}{Style.BRIGHT}"
                    "The new status is the same as the current one.\n"
                    f"{Fore.GREEN}"
                    "Status remains unchanged"
                    f"{Style.RESET_ALL}"
                    )
                print(
                    f"{Fore.YELLOW}{Style.BRIGHT}"
                    "\nOptions:\n"
                    "- Type 'back' to modify your input.\n"
                    "- Press Enter or any other key to proceed"
                    "without changes.\n"
                    "\nChoose an option:"
                    f"{Style.RESET_ALL}"
                    )
                # Direct input for local decision
                choice = input().strip().lower()
                # Allows the user to re-enter a new status
                if choice == 'back':
                    # Loop back for re-entry
                    continue
                else:
                    # If the user decides not to type 'back',
                    # just proceed without repeating the message.
                    break
            else:
                # If the new status is different from the current one,
                # update it
                worksheet.update_cell(task_index, 5, new_status)
                print(
                    f"{Fore.GREEN}{Style.BRIGHT}"
                    "Status change successful."
                    f"{Style.RESET_ALL}")
                break

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
    # Amended from: www.w3schools.com/python/python_try_except.asp
    try:
        # Prompt user for task IDs to delete, separated by commas
        task_ids_input = get_user_input(
            f"{Fore.LIGHTBLUE_EX}"
            "Enter the Task ID(s) of the tasks you want to delete"
            "(separated by commas): \n"
            f"{Style.RESET_ALL}"
        )
        # Split the input into a list of task IDs, trimming whitespace
        task_ids = [task_id.strip() for task_id in task_ids_input.split(",")]

        tasks = worksheet.get_all_records()
        tasks_to_delete = []

        # Collect rows (indexes) to delete
        for task_id in task_ids:
            found = False
            for index, task in enumerate(tasks):
                if str(task["Task ID"]) == task_id:
                    # Considering header row and 1-based indexing
                    tasks_to_delete.append(index + 2)
                    found = True
                    break
            if not found:
                print(
                    f"{Fore.RED}{Style.BRIGHT}"
                    "Error: Task ID not found.\n"
                    "Please, try again."
                    f"{Style.RESET_ALL}"
                )
                return

        if not tasks_to_delete:
            print(
                f"{Fore.RED}{Style.BRIGHT}"
                "Error: None of the specified Task IDs were found.\n"
                "Please ensure you have entered the correct Task IDs.\n"
                f"{Style.RESET_ALL}"
            )
            return

        # Confirm deletion with the user before proceeding
        confirm = input(
            f"{Fore.YELLOW}{Style.BRIGHT}"
            "Are you sure you want to delete task(s)?\n"
            "The action is irreversible! (yes/no): \n"
            f"{Style.RESET_ALL}"
        ).strip().lower()

        if confirm == "yes":
            tasks_to_delete.sort(reverse=True)
            for row in tasks_to_delete:
                try:
                    worksheet.delete_rows(row)
                    print(
                        f"{Fore.GREEN}{Style.BRIGHT}"
                        "\nTask(s) deleted successfully."
                        f"{Style.RESET_ALL}"
                    )
                except APIError as e:
                    # Print the API error
                    error_message = (
                        f"{Fore.RED}{Style.BRIGHT}"
                        "Error: Failed to delete task due"
                        "to a Google Sheets API error: "
                        f"{e}"
                        f"{Style.RESET_ALL}"
                    )
                    print(error_message, e)
        elif confirm == "no":
            print(
                f"{Fore.GREEN}{Style.BRIGHT}"
                "\nTask deletion canceled."
                f"{Style.RESET_ALL}"
            )
        else:
            print(
                f"{Fore.RED}{Style.BRIGHT}"
                "\nError: Invalid input."
                "Please answer 'yes' or 'no'."
                f"{Style.RESET_ALL}"
            )

    except ExitToMainMenu:
        return


def clear_terminal():
    """
    Amended from www.geeksforgeeks.org/clear-screen-python/
    Clear the terminal screen.
    """
    # Windows
    if os.name == 'nt':
        os.system('cls')
    # Unix/Linux/MacOS/BSD/etc
    else:
        os.system('clear')


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
        # Amended from: www.w3schools.com/python/python_try_except.asp
        try:
            print("\nMain Menu ")
            print("---------")
            print("1. Add Task")
            print("2. List All Tasks")
            print("3. View Task      (select ID from menu item 2)")
            print("4. Update Task    (select ID from menu item 2)")
            print("5. Delete Task(s) (select ID from menu item 2)")
            print("6. Clear screen")
            print("7. Exit application\n")
            choice = get_user_input(
             "Please, select option (1-7) or type 'back' to return to menu: "
            )

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
                clear_terminal()
            elif choice == "7":
                print(f"{Fore.MAGENTA}{Style.BRIGHT}"
                      "- - - Exiting the Task Organizer."
                      " Goodbye & Welcome back! - - - \n"
                      f"{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}{Style.BRIGHT}"
                      "Error: Invalid choice. \n"
                      "Please try again.\n"
                      f"{Style.RESET_ALL}")
        except ExitToMainMenu:
            # If "back" is entered at any input prompt,
            # loop back to the main menu
            continue


# ASCII Art in Magenta Color
ascii_art = [
    f"{Fore.MAGENTA}#######        ######        ",
    f"{Fore.MAGENTA}   #     ####  #     #  ####  ",
    f"{Fore.MAGENTA}   #    #    # #     # #    # ",
    f"{Fore.MAGENTA}   #     ####  ######   ####  "
]

# Printing the ASCII Art
for ascii_line in ascii_art:
    print(ascii_line)

print(
    f"{Fore.MAGENTA}{Style.BRIGHT}"
    "\nWelcome to Your Personal Task Organizer! 🌟 \n"
    f"{Style.RESET_ALL}"
)
print(
    f"{Fore.BLUE}{Style.BRIGHT}"
    "Welcome to Task Master! Streamline your to-dos with ease."
    "\nAdd, manage, and track tasks effortlessly with the simple menu-driven"
    "\ninterface. Select an option, press Enter, and you're on your way!"
    f"{Style.RESET_ALL}"
)
main_menu()
