# Amended from: www.geeksforgeeks.org/clear-screen-python/
import os

# Amended from: www.geeksforgeeks.org/python-datetime-module/
import datetime

# Amended from: Code Institute project love_sandwiches
import gspread
from google.oauth2.service_account import Credentials

# Amended from: pypi.org/project/prettytable/
from prettytable import PrettyTable

# Amended from: docs.python.org/3/library/textwrap.html
import textwrap

# Amended from: www.geeksforgeeks.org/print-colors-python-terminal/
import colorama
from colorama import Fore, Back, Style

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
    The method is chosen for its simplicity and effectiveness in environments
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
    allow_skip=False,
    numeric=False
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
        # Colorize and reset prompt color within the function
        user_input = input(Fore.BLUE + prompt + Fore.RESET).strip()

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
        due_date_str = input("Enter Due Date (YY-MM-DD): \n")
        # Amended from: www.w3schools.com/python/python_try_except.asp

        # Check for 'back' command to return or exit
        if due_date_str.lower() == "back":
            raise ExitToMainMenu

        try:
            # Amended from:
            # geeksforgeeks.org/python-datetime-strptime-function/
            due_date = datetime.datetime.strptime(
                due_date_str, "%y-%m-%d"
            ).date()

            if due_date < datetime.date.today():
                print(
                    f"{Fore.RED}{Style.BRIGHT}"
                    "\nError: The due date must be in the future.\n"
                    "Please try again."
                    f"{Style.RESET_ALL}\n"
                )
            else:
                return due_date_str  # Return the valid due date string
        except ValueError:
            print(
                f"{Fore.RED}{Style.BRIGHT}"
                "Error: Invalid date format."
                "Please use YY-MM-DD."
                f"{Style.RESET_ALL}\n"
                )


# Define allowed values for task priority and status
# to ensure user inputs are standardized and limited to these options.
priority_allowed_values = ["High", "Med", "Low"]
status_allowed_values = ["New", "Done", "Pend"]


def add_row_to_sheet():
    """
    Prompts user for task details and adds a new row to the Google Sheet.
    Fields include as listed below Due Date is validated for future
    dates in YY-MM-DD format.
    """
    # Generate & display the Task ID
    task_id = generate_task_id()
    print(f"Task ID: {task_id}")
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
    Amended from: docs.python.org/3/library/textwrap.html
    Wraps text to the specified width and returns a list of wrapped lines.
    """
    return textwrap.wrap(text, width, break_long_words=True)


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
    print("-------------")
    # Print the options with the selected header color
    print("1. Task ID (default)")
    print("2. Priority")
    print("3. Status")
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
    except Exception as e:
        print(f"An error occurred during sorting: {e}. Sorting by Task ID.")
        # Fallback to default sorting if any error occurs
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
    # Amended from: docs.python.org/3/library/textwrap.html
    max_width = 30

    for task in sorted_tasks:
        wrapped_text = wrap_text(task["To-Do"], max_width)
        num_lines = len(wrapped_text)

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
        Fore.BLUE + str(table) + Fore.RESET
        )


def view_task():
    """
    Prompts the user for a Task ID and displays the details of
    the specified task.
    """
    task_id = get_user_input("Enter Task ID to view: \n", numeric=True)
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

        # Add the found task to the table
        task_table.add_row(
            [
                found_task["Task ID"],
                found_task["To-Do"],
                found_task["Priority"],
                found_task["Due Date"],
                found_task["Status"],
                found_task["Creation Date"],
            ]
        )
        # For readability
        print()

        # Print the task details table with colored text
        print(
            Fore.BLUE + str(task_table) + Fore.RESET
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
    - Empty input for any field (except the Task ID) skips the update for
      that field, leaving the original value unchanged.
    - The function validates the Task ID and informs the user if the specified
      task cannot be found.
    - For the due date, the function checks for valid date format (YY-MM-DD)
      and skips update if the format is incorrect, without terminating the
      update process.
    - checks to notify the user if the new priority or status is the same
      as the current one, avoiding unnecessary updates.
    - Utilizes the `ExitToMainMenu` exception to allow exiting to the main menu
      at any point by typing a specific command (e.g., 'back')
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
                  f"{Style.RESET_ALL}")
            return

        print("Update Task Details:")
        print("---------------------")

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

        # Prompt for a new priority, allowing an empty input to skip
        # the update
        new_priority = get_user_input(
            "Please, enter new priority (High/Med/Low) "
            "or press key Enter to skip: \n",
            normalize=True,
            allowed_values=priority_allowed_values + [""],
            allow_skip=True,
        )

        # Notify the user if the new priority is the same as the current one.
        if (new_priority and
                new_priority.lower() == current_task["Priority"].lower()):
            confirm_change = (
                input(
                    "The new priority is the same as the current one. "
                    "Do you still want to change it? (yes/no): \n"
                )
                .strip()
                .lower()
            )

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
            "Please, enter new Due Date (YY-MM-DD) or "
            "press Enter to skip: \n",
            allow_skip=True,
        )
        if new_due_date:
            # Amended from: www.w3schools.com/python/python_try_except.asp
            try:
                # Validate the date format by attempting to convert
                # the string into a date
                due_date = datetime.datetime.strptime(
                        new_due_date, "%y-%m-%d").date()
                if due_date < datetime.date.today():
                    print(f"{Fore.RED}{Style.BRIGHT}"
                          "Due date must be in the future. Please try again."
                          f"{Style.RESET_ALL}\n")
                else:
                    worksheet.update_cell(task_index, 4, new_due_date)
            except ValueError:
                # If the date format is invalid, inform user
                # and skip updating the due date
                print("Invalid date format. Skipped updating due date.\n")

        # Ask the user for a new status, allowing an empty input
        # to skip the update
        new_status = get_user_input(
            "Please, enter new status (New/Done/Pend) or "
            "press Enter to skip: \n",
            normalize=True,
            allowed_values=status_allowed_values + [""],
            allow_skip=True,
        )

        # Notify the user if the new status is the same as the current one.
        if new_status and new_status.lower() == current_task["Status"].lower():
            # Ask the user if they want to proceed with changing the status
            # even though it's the same as the current one
            confirm_change_status = (
                input(
                    "The new status is the same as the current one."
                    " Do you still want to change it? (yes/no): "
                )
                .strip()
                .lower()
            )
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
        print(f"{Fore.GREEN}{Style.BRIGHT}"
              "Task updated successfully."
              f"{Style.RESET_ALL}")
           
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
            print(f"{Fore.RED}{Style.BRIGHT}"
                  "Error: None of the specified Task IDs were found. \n"
                  "Please ensure you have entered the correct Task IDs."
                  f"{Style.RESET_ALL}"
                  )
            return

        # Confirm deletion with the user before proceeding
        confirm = (
            input(f"{Fore.YELLOW}{Style.BRIGHT}"
                "Are you sure you want to delete these tasks?"
                " The action is irreversible! (yes/no): "
                f"{Style.RESET_ALL}"
            )
            .strip()
            .lower()
        )

        if confirm == "yes":
            # Sort the list in reverse order to avoid messing up the indexes
            tasks_to_delete.sort(reverse=True)
            # Amended from: www.w3schools.com/python/python_try_except.asp
            try:
                for row in tasks_to_delete:
                    worksheet.delete_rows(row)
                    print(f"{Fore.GREEN}{Style.BRIGHT}"
                          "\nTasks deleted successfully."
                          f"{Style.RESET_ALL}")

            except gspread.exceptions.APIError as e:
                # Print the API error
                error_message = (
                    f"{Fore.RED}{Style.BRIGHT}"
                    "Error: Failed to delete task due"
                    " to a Google Sheets API error: "
                    f"{e}"
                    f"{Style.RESET_ALL}"
                )
                print(error_message, e)

        elif confirm == "no":
            print(f"{Fore.GREEN}{Style.BRIGHT}"
                  "\nTask deletion canceled."
                  f"{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}{Style.BRIGHT}"
                  "\nError: Invalid input.\n"
                  "Please answer 'yes' or 'no'."
                  f"{Style.RESET_ALL}")

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
            print("\nMenu To-Do-List")
            print("-----------------")
            print("1. Add Task")
            print("2. List All Tasks")
            print("3. View Task")
            print("4. Update Task")
            print("5. Delete Task(s)")
            print("6. Clear screen")
            print("7. Exit application\n")
            choice = get_user_input(
                "Please, select an option (1-7): \n"
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
                      "- - - Exiting the Task Organizer. Goodbye! - - - \n"
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
for line in ascii_art:
    print(line)

print(
    f"{Fore.MAGENTA}{Style.BRIGHT}"
    "\nWelcome to Your Personal Task Organizer! 🌟 \n"
    f"{Style.RESET_ALL}"
)
print(
    f"{Fore.BLUE}{Style.BRIGHT}"
    "Manage tasks easily with our intuitive organizer."
    "\nStay focused; add, update, and track to-dos."
    "\n Get started now and make task management a breeze!"
    f"{Style.RESET_ALL}"
)

main_menu()
