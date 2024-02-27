# Task master - Your Personal Task Organizer! 🌟

![Screenshot of the application](/documentation/doc-images/amiresponsive.webp)

Visit the deployed site: [Tic-Tac-Toe](https://jaqikal.github.io/tic-tac-toe/)

- - -

## CONTENT

* [Automated Testing](#automated-testing)
  * [pep8 validator](https://pep8ci.herokuapp.com/)
* [Manual testing](#manual-testing)
  * [User Stories test](#user-stories-test)
  * [Function Testing](#function-testing)
* [DEFECTS](#defects)
  * [Unsolved issue](#unsolved-issue)
  * [Known issue](#known-issue)

- - -

Testing was ongoing throughout the entire development. I utilised CI Python Linter tool and GITPOD terminal output whilst building to pinpoint and troubleshoot any issues as I went along. The validation process adhered to the guidelines outlined in PEP8. The majority of warnings stemmed from redundant or missing whitespace, as well as instances of redundant backslashes and insufficient indentation. These issues have been addressed and rectified accordingly.

## Automated Testing

No automatic testing apart from using the pep8 validator was perfomed.

### PEP8 validator 

* [CI Python Linter](https://pep8ci.herokuapp.com/) was used to validate the python code. Result is ALL CLEAR, NO ERRORS FOUND.


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
| Quick access specific task	| Navigate to the "View Task" option on the main menu. Enter the Task ID of the task you want to review. |The app retrieves and displays all details of the specified task, including its description, priority, due date, status, and creation date. 


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
| NRM-04 | Update Task | Specified task is updated on the Google Sheet with new values for any provided task details. | Update various fields of an existing task. Changes should be verified in Google Sheets | PASS | |
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
| ERR-02 | Update Non-existent Task | Attempting to update a task that does not exist shows an error message indicating the task cannot be found. | Update a task with an ID that doesn't exist. | PASS | |
| ERR-03 | Delete Non-existent Task | Attempting to delete a task that does not exist shows an error message indicating the task cannot be found. | Delete a task with an ID that doesn't exist. | PASS | |
| ERR-04 | Add Task | Temporarily change the permissions on the Google Sheet so that the API user does not have write access and attempt to add a task. | This results in an API error (Permission Denied) when attempting to append a row. App terminates. | PASS | |

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

I lack the technical skills necessary to manually trigger rate limits by conducting numerous operations that generate API requests in a short span, or to emulate conditions of network disruptions or API unavailability. These test cases serve as a reminder that it's crucial to assess such scenarios, especially if there are plans to expand the application further.


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


*<span style="color: blue;">[Back to Content](#content)</span>*

- - -

### UNSOLVED issue

* None

*<span style="color: blue;">[Back to Content](#content)</span>*

- - -

### KNOWN issue

* None

*<span style="color: blue;">[Back to Content](#content)</span>*
- - -