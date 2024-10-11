from flask import Blueprint, render_template, request, redirect, url_for
from flask import jsonify
from sheets import get_or_create_sheet
from utils import format_time, get_git_info
from datetime import datetime
import pytz
import os
from config import SIGN_OUT_REASONS_STAFF, SIGN_OUT_REASONS_STUDENT
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

# Function to get suggestions from the CSV file
def get_personnel_suggestions(query, user_type, grade):
    suggestions = []
    with open('./env/personnel.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            full_name = f"{row['NAME']} {row['SURNAME']}"
            
            # If the query matches the name
            if query.lower() in full_name.lower():
                # If user is Staff, suggest only those without a Class Level (staff)
                if user_type == "Staff" and not row['CLASS LEVEL']:
                    suggestions.append(full_name)
                # If user is a Student, suggest those with matching Class Level
                elif user_type == "Student" and row['CLASS LEVEL'] == grade:
                    suggestions.append(full_name)

    return suggestions

@main_bp.route('/')
def index():
    # Get the git information
    commit_hash, version_tag = get_git_info()
    return render_template('index.html', commit_hash=commit_hash, version_tag=version_tag)

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
        return render_template('name.html', user_type="Student", grade=grade)  # Pass grade to next step
    return render_template('grade.html', grades=grades)

@main_bp.route('/signinout', methods=['POST'])
def signinout():
    name = request.form['guest-name']
    user_type = request.form['user_type']
    grade = request.form.get('grade', '')  # Capture the grade if available

    reasons = []
    if user_type == "Student":
        reasons = SIGN_OUT_REASONS_STUDENT
    else:
        reasons = SIGN_OUT_REASONS_STAFF

    return render_template('signinout.html', name=name, user_type=user_type, grade=grade, reasons=reasons)


@main_bp.route('/submit', methods=['POST'])
def submit():
    action = request.form['action']
    name = request.form['name']
    user_type = request.form['user_type']
    grade = request.form.get('grade', '')  # Capture the grade if available
    
    reason = request.form.get('reason', '')
    other_reason = request.form.get('other_reason', '')
    visitor_reason = request.form.get('visitor-reason', '')
    visitor_affiliation = request.form.get('visitor-affiliation', '')
    visitor_phone = request.form.get('visitor-phone', '')
    return_time = request.form.get('return_time', '')

    if other_reason:
        reason = other_reason
    elif visitor_reason:
        reason = visitor_reason

    if action == "Signing In":
        return_time = ''

    # Get current time in Vancouver timezone
    vancouver_tz = pytz.timezone('America/Vancouver')
    current_time = datetime.now(vancouver_tz)
    current_date = current_time.strftime('%Y-%m-%d')
    current_time_formatted = format_time(current_time)

    sheet_name = current_date

    # Create or get the sheet and append the row
    worksheet = get_or_create_sheet(sheet_name)
    worksheet.append_row([current_date, current_time_formatted, name, action, user_type, grade, reason, return_time, visitor_phone, visitor_affiliation])

    # Render the confirmation page after submission
    action_text = "Signed In" if action == "Signing In" else "Signed Out"
    confirmation_text = ""
    if user_type == "Visitor" and action == "Signing In":
        confirmation_text = "Sign in successful, please report to the front office."
    else:
        confirmation_text = name + " Has Successfully " + action_text + "!"

    return render_template('confirmation.html', confirmation_text=confirmation_text)


# Auto complete API calls
@main_bp.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query', '')
    user_type = request.args.get('user_type', '')
    grade = request.args.get('grade', '')

    # Fetch suggestions based on user type and grade
    suggestions = get_personnel_suggestions(query, user_type, grade)
    return jsonify(suggestions)

@main_bp.route('/student_names', methods=['GET'])
def student_names():
    grade = request.args.get('grade', '')

    # Read students from CSV
    students = []
    with open('./env/personnel.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['CLASS LEVEL'] == grade:  # Only include students in the specified grade
                full_name = f"{row['NAME']} {row['SURNAME']}"
                students.append(full_name)

    return jsonify(students)