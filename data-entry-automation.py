import pandas as pd
from openpyxl import load_workbook  # For Excel (xlsx) files
# For Google Sheets interaction (if needed)
# from googleapiclient.discovery import build
# from google.oauth2 import service_account

def data_entry_automation(input_file, output_file, sheet_name="Sheet1"):
    """
    Automates data entry from a CSV or Excel file to another Excel file.

    Args:
        input_file (str): Path to the input CSV or Excel file.
        output_file (str): Path to the output Excel file.
        sheet_name (str, optional): Name of the sheet in the output Excel file. Defaults to "Sheet1".
    """

    try:
        # 1. Read Data from Input File
        if input_file.endswith(".csv"):
            df = pd.read_csv(input_file)
        elif input_file.endswith((".xls", ".xlsx")):  # Handle both xls and xlsx
            df = pd.read_excel(input_file)  # Or pd.read_excel(input_file, engine='openpyxl') if needed
        else:
            raise ValueError("Unsupported input file format.  Please provide a CSV or Excel file.")


        # 2. Data Transformation/Cleaning (Optional, but highly recommended)
        # Example: Fill missing values
        df.fillna("", inplace=True)  # Replace NaN with empty strings
        # Example: Convert data types (if necessary)
        # df['DateColumn'] = pd.to_datetime(df['DateColumn'])
        # ... other cleaning or transformation steps as needed ...

        # 3. Write Data to Output Excel File
        try:
            # Try to open the output file to append if it exists
            book = load_workbook(output_file)
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False, if_sheet_exists='replace') # 'replace', 'append', 'new'
        except FileNotFoundError:
            # If the file doesn't exist, create a new one
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Data successfully entered into {output_file}, sheet '{sheet_name}'.")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example Usage (replace with your actual file paths)
input_file_path = "input_data.csv"  # Or "input_data.xlsx"
output_file_path = "output_data.xlsx"
sheet_name_to_use = "DataEntrySheet"

data_entry_automation(input_file_path, output_file_path, sheet_name_to_use)


# --- Example for Google Sheets (If needed. Requires setting up API credentials) ---
# def data_entry_to_gsheet(df, spreadsheet_id, sheet_name):
#     # ... (Google Sheets API interaction using gspread or googleapiclient) ...
#     # This part is more complex and requires authentication.  You can find examples online.
#     pass # Placeholder
