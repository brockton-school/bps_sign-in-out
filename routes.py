from flask import Blueprint, render_template, request, redirect, url_for
from sheets import get_or_create_sheet
from utils import format_time
from datetime import datetime
import pytz
import os
from config import SIGN_OUT_REASONS
import csv

main_bp = Blueprint('main', __name__)

# Function to read grades from the CSV file
def read_grades_from_csv(file_path):
    grades = []
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            grades.append(row[0])
    return grades

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/name', methods=['POST'])
def name():
    user_type = request.form['user_type']
    if user_type == "Student":
        return redirect(url_for('main.grade'))  # Redirect to grade selection for students
    return render_template('name.html', user_type=user_type)  # Staff/Visitor flow remains the same

@main_bp.route('/grade', methods=['GET', 'POST'])
def grade():
    grades = read_grades_from_csv('/app/grades.csv')  # Read grades from the mounted CSV file
    if request.method == 'POST':
        grade = request.form['grade']
        name = request.form.get('name', '')
        return render_template('name.html', user_type="Student", grade=grade)  # Pass grade to next step
    return render_template('grade.html', grades=grades)

@main_bp.route('/signinout', methods=['POST'])
def signinout():
    name = request.form['name']
    user_type = request.form['user_type']
    grade = request.form.get('grade', '')  # Capture the grade if available
    return render_template('signinout.html', name=name, user_type=user_type, grade=grade, reasons=SIGN_OUT_REASONS)


@main_bp.route('/submit', methods=['POST'])
def submit():
    action = request.form['action']
    name = request.form['name']
    user_type = request.form['user_type']
    grade = request.form.get('grade', '')  # Capture the grade if available
    
    reason = request.form.get('reason', '')
    other_reason = request.form.get('other_reason', '')
    visitor_reason = request.form.get('visitor-reason', '')

    if other_reason:
        reason = other_reason
    elif visitor_reason:
        reason = visitor_reason

    # Get current time in Vancouver timezone
    vancouver_tz = pytz.timezone('America/Vancouver')
    current_time = datetime.now(vancouver_tz)
    current_date = current_time.strftime('%Y-%m-%d')
    current_time_formatted = format_time(current_time)

    sheet_name = current_date

    # Create or get the sheet and append the row
    worksheet = get_or_create_sheet(sheet_name)
    worksheet.append_row([current_date, current_time_formatted, name, action, user_type, grade, reason])

    # Render the confirmation page after submission
    action_text = "Signed In" if action == "Signing In" else "Signed Out"
    confirmation_text = ""
    if user_type == "Visitor":
        confirmation_text = "Sign in successful, please report to the front office."
    else:
        confirmation_text = name + " Has Successfully " + action_text

    return render_template('confirmation.html', confirmation_text=confirmation_text)


