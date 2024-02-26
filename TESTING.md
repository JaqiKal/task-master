
Tested to open a worksheet that does not exist, by renaming my google doc spreadsheet tab to 'test-sheet-x", hence the database is not existing anymore. This raised "gspread.exceptions.WorksheetNotFound: 'name of my worksheet' " error. 

```
# Google Sheets setup
CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("task-master-database")
worksheet = SHEET.worksheet("taskdb")
```

To handle this I added try-except block around the operation that might fail. This code will try to open the worksheet named 'taskdb'. If the worksheet is not found, it will catch the WorksheetNotFound exception, print an error message, and exit the program.
```
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
