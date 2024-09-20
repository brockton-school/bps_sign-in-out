import gspread
import os
from google.oauth2.service_account import Credentials
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime  # Import datetime module
import pytz  # Import pytz to handle timezones
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

# Load environment variables for Google Sheets ID and Credentials JSON path
GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
SERVICE_ACCOUNT_FILE = os.getenv('GOOGLE_CREDENTIALS_PATH')

# Define preset options for the "reason"
SIGN_OUT_REASONS = ["Lunch", "Sick", "Appointment"]

app = Flask(__name__)

# Add ProxyFix middleware to handle reverse proxy headers
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

# Authenticate with Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
CREDS = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Connect to the Google Sheet
gc = gspread.authorize(CREDS)
spreadsheet = gc.open_by_key(GOOGLE_SHEET_ID)

def get_or_create_sheet(spreadsheet, sheet_name):
    """Check if a sheet with the given name exists, otherwise create it."""
    try:
        worksheet = spreadsheet.worksheet(sheet_name)
    except gspread.exceptions.WorksheetNotFound:
        worksheet = spreadsheet.add_worksheet(title=sheet_name, rows="100", cols="6")
        worksheet.append_row(["User Type", "Name", "Action", "Date", "Time", "Reason"])  # Add headers

        # Bold the header row and freeze it
        bold_format = {
            "repeatCell": {
                "range": {
                    "sheetId": worksheet.id,
                    "startRowIndex": 0,
                    "endRowIndex": 1  # The first row
                },
                "cell": {
                    "userEnteredFormat": {
                        "textFormat": {"bold": True}
                    }
                },
                "fields": "userEnteredFormat.textFormat.bold"
            }
        }

        freeze_row_request = {
            "updateSheetProperties": {
                "properties": {
                    "sheetId": worksheet.id,
                    "gridProperties": {
                        "frozenRowCount": 1  # Freeze the first row
                    }
                },
                "fields": "gridProperties.frozenRowCount"
            }
        }

        # Conditional formatting for Action column (sign-ins green, sign-outs red)
        conditional_formatting_action = {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": worksheet.id,
                            "startColumnIndex": 2,  # Action column (column C)
                            "endColumnIndex": 3
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "TEXT_EQ",
                            "values": [{"userEnteredValue": "Signing In"}]
                        },
                        "format": {
                            "backgroundColor": {"red": 0.8, "green": 1, "blue": 0.8}
                        }
                    }
                },
                "index": 0
            }
        }

        conditional_formatting_sign_out = {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": worksheet.id,
                            "startColumnIndex": 2,  # Action column (column C)
                            "endColumnIndex": 3
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "TEXT_EQ",
                            "values": [{"userEnteredValue": "Signing Out"}]
                        },
                        "format": {
                            "backgroundColor": {"red": 1, "green": 0.8, "blue": 0.8}
                        }
                    }
                },
                "index": 1
            }
        }

        # Conditional formatting for User Type column (staff yellow, students blue)
        conditional_formatting_user_type = {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": worksheet.id,
                            "startColumnIndex": 0,  # User Type column (column A)
                            "endColumnIndex": 1
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "TEXT_EQ",
                            "values": [{"userEnteredValue": "Staff"}]
                        },
                        "format": {
                            "backgroundColor": {"red": 1, "green": 1, "blue": 0.8}  # Light yellow
                        }
                    }
                },
                "index": 0
            }
        }

        conditional_formatting_student = {
            "addConditionalFormatRule": {
                "rule": {
                    "ranges": [
                        {
                            "sheetId": worksheet.id,
                            "startColumnIndex": 0,  # User Type column (column A)
                            "endColumnIndex": 1
                        }
                    ],
                    "booleanRule": {
                        "condition": {
                            "type": "TEXT_EQ",
                            "values": [{"userEnteredValue": "Student"}]
                        },
                        "format": {
                            "backgroundColor": {"red": 0.8, "green": 0.8, "blue": 1}  # Light blue
                        }
                    }
                },
                "index": 1
            }
        }

        # Apply the formatting requests and conditional formatting in a single batch update
        spreadsheet.batch_update({
            "requests": [
                bold_format,
                freeze_row_request,
                conditional_formatting_action,
                conditional_formatting_sign_out,
                conditional_formatting_user_type,
                conditional_formatting_student
            ]
        })

    return worksheet




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/name', methods=['POST'])
def name():
    user_type = request.form['user_type']
    return render_template('name.html', user_type=user_type)

@app.route('/signinout', methods=['POST'])
def signinout():
    name = request.form['name']
    user_type = request.form['user_type']
    return render_template('signinout.html', name=name, user_type=user_type, reasons=SIGN_OUT_REASONS)

@app.route('/submit', methods=['POST'])
def submit():
    action = request.form['action']
    name = request.form['name']
    user_type = request.form['user_type']
    
    # Capture reason, prioritize "other_reason" if provided
    reason = request.form.get('reason', '')
    other_reason = request.form.get('other_reason', '')
    if other_reason:
        reason = other_reason

    # Define the Vancouver time zone
    vancouver_tz = pytz.timezone('America/Vancouver')

    # Get the current date and time in Vancouver time zone
    current_time = datetime.now(vancouver_tz)
    current_date = current_time.strftime('%Y-%m-%d')  # Format date as YYYY-MM-DD
    current_time_formatted = current_time.strftime('%I:%M %p')  # 1:29 PM format

    # Use the current date as the sheet name (e.g., "2024-09-20")
    sheet_name = current_date

    # Get the sheet for the current date or create one if it doesn't exist
    worksheet = get_or_create_sheet(spreadsheet, sheet_name)

    # Append the data to the sheet (including reason if provided)
    worksheet.append_row([user_type, name, action, current_date, current_time_formatted, reason])

    # Fix the grammar of the action: "Signing In" -> "Signed In" and "Signing Out" -> "Signed Out"
    if action == "Signing In":
        action_text = "signed in"
    elif action == "Signing Out":
        action_text = "signed out"
    
    # Pass the corrected action text and name to the confirmation page
    return render_template('confirmation.html', name=name, action_text=action_text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
