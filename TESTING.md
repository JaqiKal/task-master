# Task master - Your Task Organizer! 🌟

![x](/documentation/images/landingpage.webp)

Visit the deployed application at [Heroku](https://task-maestro-fc8139fbc4e1.herokuapp.com/)

- - -

## CONTENT

* [Testing overview & environment](#testing-overview--environment)
  * [Test environment](#test-environment)
  * [Browser compatibilty](#browser-compatibilty)
  * [Responsiveness](#responsiveness)
* [Automated Testing](#automated-testing)
  * [pep8 validator](https://pep8ci.herokuapp.com/)
* [Manual testing](#manual-testing)
  * [User Stories test](#user-stories-test)
  * [Function Testing](#function-testing)
* [DEFECTS](#defects)
  * [Unsolved issue](#unsolved-issue)
  * [Known issue](#known-issue)

- - -
## Testing overview & environment

Testing was ongoing throughout the entire development. I used the CI Python Linter tool and GITPOD terminal output whilst building to pinpoint and troubleshoot any issues as I went along. The validation process adhered to the guidelines outlined in PEP8. The majority of warnings stemmed from redundant or missing whitespace, as well as instances of redundant backslashes and insufficient indentation. These issues have been addressed and rectified accordingly.

### Test environment

* Desktop:
  * Lenovo Legion T7
* Screen:
  * Samsung Odyssey G3 / 27" / 1920 x 1080 /

### Browser compatibility

* Google Chrome, version 121.0.6167.86 (Official Build) (64-bit)
* Firefox, version 123.0 (64-bit)

### Responsiveness

Although not directly applicable to this project, I gained valuable knowledge on adjusting the mock terminal window size. This exploration allowed me to enhance the user interface with a more friendly table display. However, to maintain consistency with Code Institute's settings and requirements, I ultimately reverted these adjustments. Instead, I tailored my code to conform to the given limits of the mock terminal environment. This experience underscored the importance of adaptability and optimization within predefined constraints, enriching my understanding of creating user-centric interfaces within specific technical boundaries.

## Automated Testing

No automatic testing apart from using the pep8 validator was performed.

### PEP8 validator 

* [CI Python Linter](https://pep8ci.herokuapp.com/) was used to validate the python code. The result is ALL CLEAR, NO ERRORS FOUND.

![x](/documentation/images/pep8.webp)

*<span style="color: blue;">[Back to Content](#content)</span>*

- - -

## Manual test

### User Stories test

`First Time Visitors`

|  Goals | Expected Outcome | Testing Performed | Result |
| :--- | :--- | :--- | :--- |
| Understand Purpose | Manually open the app's landing page and verify if there is a clear description or welcome message explaining the purpose of the task organizer. | Manually opened the landing page and checked for a descriptive welcome message or title.  | PASS |
| Understand Purpose | Check for the presence of a descriptive title or introductory text prominently displayed on the landing page. | Verified the existence of a descriptive title or introductory text on the landing page. | PASS |
| Intuitive UI | Manually navigate through the app's menu and verify if labels are easy to understand and instructions are straightforward.| Manually navigated through the menu and assessed the clarity of labels and instructions. | PASS |
|Intuitive UI | Attempt to perform basic tasks such as adding a new task, updating an existing task, and deleting a task to verify ease of use. | Attempted basic tasks like adding, updating, and deleting tasks to evaluate user experience. | PASS |

`Returning Visitors`

|  Goals | Expected Outcome | Testing Performed | Result |
| :--- | :--- | :--- | :--- |
| Quick access specific task	| Navigate to the "View Task" option on the main menu. Enter the Task ID of the task you want to review. |The app retrieves and displays all details of the specified task, including its description, priority, due date, status, and creation date. | PASS |


`Frequent Visitors`

|  Goals | Expected Outcome | Testing Performed | Result |
| :--- | :--- | :--- | :--- |
| Efficiently update existing tasks	| Utilize the "Update Task" functionality from the main menu. Selectively modify task details such as description, priority, due date, and status as needed. |The app retrieves and Upon successful updates, users receive confirmation, ensuring tasks are updated quickly and efficiently.  | PASS |



*<span style="color: blue;">[Back to Content](#content)</span>*

- - -

### Function Testing

#### Normal Test Case (NRM)

| TestCase ID | Feature | Expected Outcome | Testing Performed | Result | Comment |
|---|---|---|---|---|---|
| NRM-01 | Add Task | A new row is added to the Google Sheet with task details and a unique, auto-generated task ID. | Fill in the prompted fields and submit the task. | PASS | |
| NRM-02 | List All Tasks | All tasks from the Google Sheet are displayed in a formatted table with details including Task ID, description, and dates.| Select the option to list all tasks. | PASS | |
| NRM-03 | View Specific Task | Details of the specified task are displayed, including Task ID, description, priority, due date, status, and creation date.| Enter a Task ID to view its details. Ensure Task ID exists | PASS |  |
| NRM-04 | Update Task | The specified task is updated on the Google Sheet with new values for any provided task details. | Update various fields of an existing task. Changes should be verified in Google Sheets | PASS | |
| NRM-05 | Delete Task | The specified tasks are deleted from the Google Sheet. | Delete specific task(s) by entering Task ID(s). | PASS | |
| NRM-06 | Multiple Tasks Deletion| Successfully deletes multiple specified tasks from the Google Sheet. | Delete multiple tasks by entering their IDs separated by commas. | PASS | |

#### Input validation Test (IPU)

| TestCase ID | Feature | Expected Outcome | Testing Performed | Result | Comment |
|---|---|---|---|---|---|
| IPU-01 | Empty Task Description | The application prevents adding a task with an empty description and displays an error message.| Attempt to add a task without a description. | PASS | |
| IPU-02 | Future Due Date  | The application only accepts future dates for the due date field and displays an error message for past dates. | Enter a past date as the due date for a new task. | PASS | |
| IPU-03 | Invalid Date Format | The application displays an error message for due dates not in the YYYY-MM-DD format. | Enter a due date in an incorrect format. | PASS | |
| IPU-04 | Invalid Priority Input | Entering an invalid priority shows an error message and does not update the task.| Try to update a task with an invalid priority value. | PASS | |
| IPU-05 | Invalid Status Input   | Entering an invalid status shows an error message and does not update the task. | Try to update a task with an invalid status value. | PASS | |
| IPU-06 | Invalid Input Handling | General invalid inputs for any field should be handled gracefully with an error message. | Enter various invalid inputs in different fields. | PASS | |

#### Error Handling (ERR)

| TestCase ID | Feature | Expected Outcome | Testing Performed | Result | Comment |
|---|---|---|---|---|---|
| ERR-01 | Invalid Task ID | For invalid Task ID inputs, the application prevents action and displays an error message. ID.  | Attempt actions with non-existent Task ID. | PASS | |
| ERR-02 | Update non-existent Task | Attempting to update a task that does not exist shows an error message indicating the task cannot be found. | Update a task with an ID that doesn't exist. | PASS | |
| ERR-03 | Delete Non-existent Task | Attempting to delete a task that does not exist shows an error message indicating the task cannot be found. | Delete a task with an ID that doesn't exist. | PASS | |
| ERR-04 | Add Task | Temporarily change the permissions on the Google Sheet so that the API user does not have write access and attempts to add a task. | This results in an API error (PERMISSION_DENIED) when attempting to append a row. App terminates. | PASS | |

#### User Interaction Test (UIA)

| TestCase ID | Feature | Expected Outcome | Testing Performed | Result | Comment |
|---|---|---|---|---|---|
| UIA-01 |  View Empty Task List | Displays a message indicating no tasks are found if the task list is empty. | Attempt to list or view tasks when none exist. | PASS | |
| UIA-02 |  Skip Update Field | Skipping input (by pressing Enter) during an update operation leaves the original value unchanged. | Attempt to update a task but skip fields by pressing Enter. | PASS | |
| UIA-03 |  Application Exit | The application closes without error when selecting the exit option. | Choose the exit option from the main menu. | PASS | |

#### Integration Test (ITC)

| TestCase ID | Feature | Expected Outcome | Testing Performed | Result | Comment |
|---|---|---|---|---|---|
| ITC-01 | Google Sheets API Connection | The application successfully connects to the Google Sheets API and retrieves data without errors. | Attempt to connect to the Google Sheets API and request data. | PASS | |
| ITC-02 | Data Sync with Google Sheets | All changes made via the application are accurately reflected in the Google Sheets document. | Add, update, and delete tasks using the application, then verify changes in Google Sheets. | PASS | |                                          |
| ITC-03 | Handling API Rate Limits | The application gracefully handles rate limit errors by queueing requests or notifying the user. | Simulate conditions where the API's rate limits are exceeded.  | Not exec |  See comment<sup>1</sup>|
| ITC-04 | Recovery from API Disruptions | The application provides informative feedback to the user and attempts reconnection or data sync when possible. | Simulate an API disruption or outage and observe application response. | Not Exec | See comment<sup>1</sup> | 

#### Comment<sup>1</sup>

I lack the technical skills necessary to manually trigger rate limits by conducting numerous operations that generate API requests in a short span or to emulate conditions of network disruptions or API unavailability. These test cases serve as a reminder that it's crucial to assess such scenarios, especially if there are plans to expand the application further.


*<span style="color: blue;">[Back to Content](#content)</span>*

### Failed  test cases

None

*<span style="color: blue;">[Back to Content](#content)</span>*

## DEFECTS

### Bug-01

I tested the scenario of attempting to open a non-existent worksheet by renaming the tab in my Google Sheets document to 'taskdbx', rendering the database inaccessible. This resulted in a ```gspread.exceptions.WorksheetNotFound``` error.

#### Solution-Bug-01
To address this issue, I implemented a try-except block to handle potential failures. The code attempts to open the worksheet named 'taskdb'. If the worksheet is not found, it catches the 'WorksheetNotFound' exception, prints an error message, and exits the program.

```python
# Google Sheets setup
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("task-master-database")
# Attempt to open the worksheet
try:
    worksheet = SHEET.worksheet("taskdb")
    # If the worksheet is found, continue with the program
except gspread.WorksheetNotFound:
    # If the worksheet is not found, print an error message and exit
    print("Error: Worksheet not found")
    exit()
```

### Bug-02

As mentioned in the [chapter Responsiveness](#responsiveness) I returned to the original size of the mock terminal. This necessitated altering the presentation format of information within the table upon rendering. During testing to ensure these modifications worked as planned, I discovered that the To-Do column had to be limited to 30 characters to prevent strings and integers from exceeding the column boundaries, which would otherwise completely disrupt the table's structure. 

![x](/documentation/images/table-no_wrap.webp)

### Solution Bug-02

The problem was solved by introducing a new function, ```def wrap_text(text, width):```, and updating the ```def list_all_tasks():``` function. These modifications implement text wrapping, which automatically divides longer text lines at a specified maximum character limit. This ensures that text remains within a readable width, enhancing the presentation and readability of the information displayed.

![x](/documentation/images/table-wrap.webp)

### Bug-03

In 'Menu To-Do-List' I select '2. List All tasks' and then hit enter to select 'sort by Task ID'. which results in the fault message:

![x](/documentation/images/wrap_text-fail.webp)

It seemed the problem arose when attempting to wrap text that is not a string, specifically when task["To-Do"] is an integer or contains integer values that are not automatically converted to string types by the wrap_text function or the textwrap.wrap method within it. I assumed this likely happens if a task's "To-Do" field is purely numeric and not explicitly cast to a string before being passed to wrap_text.

### Solution Bug-03
Edit: In a later version, lib textwrap was removed and a function was refactored with custom code, which still converts to string.

I assumed that the most direct way to solve this issue was to ensure that any value passed to wrap_text was explicitly converted to a string, regardless of its original type. I modified the wrap_text function to automatically convert its input to a string, ensuring compatibility with all types of input.

```python
def wrap_text(text, width):
    """
    Amended from: docs.python.org/3/library/textwrap.html
    Wraps text to the specified width and returns a list of wrapped lines.
    Ensures that the text is treated as a string to avoid errors with non-string inputs.
    """
    # Ensure the input is treated as a string to prevent errors
    text = str(text)
    return textwrap.wrap(text, width, break_long_words=True)
```

### Bug-04

During the task update process, I encountered an issue when prompted to enter a new date or choose to skip this step. Specifically, if an incorrect date was input—either due to being in the wrong format or not being set in the future—the application would incorrectly proceed to the next prompt, which asks to enter a new status. This behaviour bypassed the opportunity for the user to correct the date input, potentially leading to incomplete or inaccurate task updates.

![x](/documentation/images/bug04.webp)

### Solution Bug-04

To address this issue, I've refactored the code to ensure that users are now looped back to the "Enter a new status" prompt if they input an incorrect date. This revision introduces built-in loops for immediate error correction and provides users with the option to skip updating if they choose. The original implementation aimed to abstract the input gathering process to improve code organization. While this approach was intended to create a more structured codebase, it inadvertently made user retries more complicated. The latest code adjustments aim to strike a better balance between code organization and user interaction fluidity.

![x](/documentation/images/bug04-s.webp)

### Bug-05

 PrettyTable output overflow, when entering a long string of empty characters.
 
 ### Solution Bug-05

 Code has been modified to strip leading and trailing spaces from the input text before wrapping. It checks if the stripped text is empty and returns an empty list if so, ensuring that long empty strings are handled more gracefully. 

### Bug-06

In the "update task" functionality, when adding a new due date, the system accepts the input in the YY-M-D format, which is inconsistent with the desired YY-MM-DD format.

### Solution Bug-06

Implement validation by splitting the input string by - to separate year, month, and day components. Then, check if each component meets the expected length: two digits for the year, two digits for the month, and two digits for the day. If the input does not conform to these expectations, introduce a new error message to inform the user. This ensures the due date is strictly in the YY-MM-DD format, enhancing data consistency and preventing format-related errors. This solution  standardizes date input across the application, promoting uniformity and reducing potential confusion for users.

### Bug-07

When attempting to delete tasks I encountered a peculiar issue. Initially, I entered 4 task IDs without commas, which was correctly identified as an error by the system. However, when I attempted to delete these tasks by entering the IDs with commas but incorrectly specifying the task IDs, the system still deleted the four most recent tasks. This behavior suggests that the system might not be correctly identifying and processing the task IDs entered by the user, leading to unintended deletion of tasks.

### Solution Bug-07

The revised code adds a step to verify that each task ID entered by the user exists before proceeding with the deletion. This ensures that the function does not attempt to delete tasks that do not exist, which could lead to confusion or errors.

*<span style="color: blue;">[Back to Content](#content)</span>*

- - -

### UNSOLVED issue 

* In the current version of the app, entering 'back' during task update redirects users to the main menu rather than the previous step, which isn't ideal for user experience. This issue will be addressed and corrected in future updates.

* When users quickly enter selections in the Task Master application, an issue arises where input can overlap with existing text on the console. This problem seems to stem from the way the application handles asynchronous input and output operations, leading to a situation where the console output does not synchronize correctly with user inputs. As a result, the user experience is negatively impacted, with the terminal display becoming cluttered and confusing. This issue will be addressed and corrected in future updates. 

![x](/documentation/images/overlap.webp)

* Currently, the Task Master application operates without user-specific login functionality, limiting its ability to support multiple users simultaneously. This presents a challenge for environments where task management needs to be personalized or shared among team members. 

* If the application frequently interacts with Google Sheets, reaching API rate limits could lead to temporary disruptions. 

* The application currently does not implement user-specific authentication for accessing the Google Sheets backend.

* As of the current version, the Task Master application has not been comprehensively evaluated for accessibility features, including screen reader compatibility, colour contrast, and keyboard navigation, which are crucial for users with disabilities. I recognize the importance of making the application accessible to all users and am committed to improving these aspects in future updates.

* In developing the app, I employed Pylint (v2023.10.1) which flagged the use of a broad try-except block with "Catching too general exception Exception." Despite the general advice against catching broad exceptions, I opted for this method for several reasons, fully aware of the best practices. This decision balances robustness and user-friendliness, ensuring that users are shielded from raw Python errors with more accessible error messages. It's particularly vital for managing unforeseen errors from external dependencies like Google Sheets API, where issues like API limits can arise. Recognizing the challenge of covering all potential errors from various sources, this approach serves as a safeguard against unhandled crashes, enhancing user experience. I'm committed to evolving this strategy as the application and its error handling capabilities develop.

*<span style="color: blue;">[Back to Content](#content)</span>*

- - -

### KNOWN issue 

None identified

*<span style="color: blue;">[Back to Content](#content)</span>*

- - -