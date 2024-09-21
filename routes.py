from flask import Blueprint, render_template, request, redirect, url_for
from sheets import get_or_create_sheet
from utils import format_time
from datetime import datetime
import pytz
import os
from config import SIGN_OUT_REASONS

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/name', methods=['POST'])
def name():
    user_type = request.form['user_type']
    return render_template('name.html', user_type=user_type)

@main_bp.route('/signinout', methods=['POST'])
def signinout():
    name = request.form['name']
    user_type = request.form['user_type']
    return render_template('signinout.html', name=name, user_type=user_type, reasons=SIGN_OUT_REASONS)

@main_bp.route('/submit', methods=['POST'])
def submit():
    action = request.form['action']
    name = request.form['name']
    user_type = request.form['user_type']
    
    reason = request.form.get('reason', '')
    other_reason = request.form.get('other_reason', '')
    if other_reason:
        reason = other_reason

    # Get current time in Vancouver timezone
    vancouver_tz = pytz.timezone('America/Vancouver')
    current_time = datetime.now(vancouver_tz)
    current_date = current_time.strftime('%Y-%m-%d')
    current_time_formatted = format_time(current_time)

    sheet_name = current_date

    # Create or get the sheet and append the row
    worksheet = get_or_create_sheet(sheet_name)
    worksheet.append_row([current_date, current_time_formatted, name, action, user_type, reason])

    # Render the confirmation page after submission
    action_text = "Signed In" if action == "Signing In" else "Signed Out"
    return render_template('confirmation.html', name=name, action_text=action_text)