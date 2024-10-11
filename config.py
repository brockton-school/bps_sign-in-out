import os

# Google Sheets configuration
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')

# Define constants for column indices (0-based indexing)
COLUMN_DATE = 0        # A
COLUMN_TIME = 1        # B
COLUMN_NAME = 2        # C
COLUMN_ACTION = 3      # D
COLUMN_USER_TYPE = 4   # E
COLUMN_GRADE = 5       # F
COLUMN_REASON = 6      # G
COLUMN_RETURN_TIME = 7 # H
COLUMN_PHONE = 8       # I
COLUMN_AFFILIATION = 9 # J

COLUMN_HEADERS_ARRAY = ["Date", "Time", "Name", "Action", "User Type", "Grade", "Reason", "Return Time", "Visitor Phone", "Visitor Affiliation"]

COLUMNS_TOTAL = "9"

# Define preset options for the "reason"
SIGN_OUT_REASONS_STAFF      = ["Lunch", "Sick", "Appointment", "Meeting", "Field Trip"]
SIGN_OUT_REASONS_STUDENT    = ["Lunch", "Sick", "Appointment"]
# Remember to send parent contact to school for sick, or appointment

# Define preset Return Times
DEFAULT_RETURN_TIMES = ["None"]
# TODO: Set this up!!!
