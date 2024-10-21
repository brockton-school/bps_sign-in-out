import subprocess
import os
import csv

from config import PERSONNEL_CSV_PATH

def format_time(datetime_obj):
    """Formats a datetime object into a 12-hour time string."""
    return datetime_obj.strftime('%I:%M %p')

def get_git_info():
    # Get commit hash and version tag from environment variables
    commit_hash = os.getenv('COMMIT_HASH', 'Unknown')
    version_tag = os.getenv('VERSION_TAG', 'Unknown')
    return commit_hash, version_tag

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
    with open(PERSONNEL_CSV_PATH, 'r') as csvfile:
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

# Function to load users from the CSV file
def load_users_from_csv(filepath="users.csv"):
    print(filepath)
    users = {}
    try:
        with open(filepath, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 2:
                    username, hashed_password = row
                    users[username] = hashed_password
    except FileNotFoundError:
        print(f"User credentials file not found: {filepath}")
    return users

USERS = load_users_from_csv()