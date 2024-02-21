import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

# Google Sheets API setup
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("task-master-database")

# Access the 'taskdb' worksheet
taskdb = SHEET.worksheet('taskdb')

# Access the 'test_1' worksheet
test_1 = SHEET.worksheet('test_1')

# Access the 'test_2' worksheet
test_2 = SHEET.worksheet('test_2')

# List all worksheets in the spreadsheet
for worksheet in SHEET.worksheets():
    print(worksheet.title)

# Fetch the first row of the 'taskdb' worksheet (headers)
headers = taskdb.row_values(1)
print("Worksheet headers in 'taskdb':", headers)

# Fetch the first row from 'test_1'
first_row_test_1 = test_1.row_values(1)
print("First row in 'test_1':", first_row_test_1)

# Fetch the second row from 'test_1'
second_row_test_1 = test_1.row_values(2)
print("Second row in 'test_1':", second_row_test_1)

# Fetch the first row from 'test_2'
second_row_test_2 = test_2.row_values(2)
print("Second row in 'test_2':", second_row_test_2)

# Fetch all data from 'test_2'
all_data_test_2 = test_2.get_all_values()
print("All data in 'test_2':")
for row in all_data_test_2:
    print(row)