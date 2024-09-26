import os

# Google Sheets configuration
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH')

# Define constants for column indices (0-based indexing)
COLUMN_DATE = 0       # A
COLUMN_TIME = 1       # B
COLUMN_NAME = 2       # C
COLUMN_ACTION = 3     # D
COLUMN_USER_TYPE = 4  # E
COLUMN_GRADE = 5      # F
COLUMN_REASON = 6     # G

COLUMN_HEADERS_ARRAY = ["Date", "Time", "Name", "Action", "User Type", "Grade", "Reason"]

# Define preset options for the "reason"
SIGN_OUT_REASONS = ["Lunch", "Sick", "Appointment"]
