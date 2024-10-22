import subprocess
import os
import csv

from config import PERSONNEL_CSV_PATH

def format_time(datetime_obj):
    """Formats a datetime object into a 12-hour time string."""
    return datetime_obj.strftime('%I:%M %p')

def get_version_info():
    try:
        # Define the path to the version info file
        version_file_path = "/app/version_info.txt"
        
        # Open and read the file
        with open(version_file_path, "r") as file:
            version_info = file.read().strip()
        
        return version_info
    except FileNotFoundError:
        # Return a default message if the file is not found
        return "Version information not available"

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