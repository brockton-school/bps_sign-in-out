import pandas as pd
import os
from datetime import datetime
import openpyxl

from config import LOCAL_STORAGE_PATH

def save_to_local_file(entry):
    """Save the entry to a local Excel file."""
    # Create a directory structure based on year and month
    now = datetime.now()
    year = now.strftime("%Y")
    month = now.strftime("%B")
    day = now.strftime("%Y-%m-%d")

    # Define the directory and file path
    directory_path = os.path.join(LOCAL_STORAGE_PATH, year, month)
    os.makedirs(directory_path, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(directory_path, f"{day}.xlsx")

    # Create a DataFrame for the entry
    df = pd.DataFrame([entry])

    # If the file exists, append the new data; otherwise, create a new file with headers
    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        updated_df.to_excel(file_path, index=False)
    else:
        df.to_excel(file_path, index=False)