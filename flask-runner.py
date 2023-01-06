from flask import Flask
import os
from dotenv import load_dotenv
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
load_dotenv()

app = Flask(__name__)

@app.route('/test')
def run_script():
    # Define the info dictionary
    info = {
        "client_id": os.environ.get('CLIENT_ID'),
        "client_secret": os.environ.get('CLIENT_SECRET'),
        "refresh_token": os.environ.get('REFRESH_TOKEN'),
        "token_uri": os.environ.get('TOKEN_URI'),
        "user_agent": os.environ.get('USER_AGENT'),
    }

    # Jira API endpoint and token
    api_endpoint = os.environ.get('API_ENDPOINT')
    username = os.environ.get('JIRA_USERNAME')
    print(username)
    password = os.environ.get('PASSWORD')

    # Google Sheets document and sheet to read from
    spreadsheet_id = os.environ.get('SPREADSHEET_ID')
    sheet_name = os.environ.get('SHEET_NAME')

    # Columns in the sheet
    columns = ["Name", "Ticket Number", "Branch Name", "Dev Done", "Alpha Done", "Master Merged", "Status", "Description"]

    # Row in the sheet to start reading from
    start_row = 2

    def fetch_issue_data(issue_key):
        """Fetches data for a Jira issue and returns it as a dictionary"""
        url = api_endpoint.format(issue_key)
        response = requests.get(url, auth=(username,password))
        data = response.json()
        print(data)
        return {
            "Name": data["fields"]["creator"]["displayName"],
            "Ticket Number": data["key"],
            "description": data["fields"]["description"],
            "status": data["fields"]["status"]["name"],
        }

    def write_data_to_sheet(data, row):
        """Writes data to a Google Sheets document at a specific row"""
        # Set up the Sheets API client
        creds = Credentials.from_authorized_user_info(info)
        service = build("sheets", "v4", credentials=creds)
        # Build the request body
        values = [[data[column] for column in columns]]
        body = {"values": values}

        # Write the data to the sheet
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=f"{sheet_name}!A{row}:H{row}",
            valueInputOption="RAW",
            body=body
        ).execute()

    # Set up the Sheets API client
    creds = Credentials.from_authorized_user_info(info)
    service = build("sheets", "v4", credentials=creds)

    # Read ticket numbers from the "Ticket Number" column in the sheet
    service = build("sheets", "v4", credentials=creds)
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!B{start_row}:B"
    ).execute()
    ticket_numbers = result["values"]

    # Fetch data for each ticket and write it to the sheet
    for i, ticket_number in enumerate(ticket_numbers):
        data = fetch_issue_data(ticket_number[0])
        description = data["description"]
        parts = description.split("|")
        branch_name = parts[6] if len(parts) > 6 else ""
        dev_done = parts[7] if len(parts) > 7 else ""
        alpha_done = parts[8] if len(parts) > 8 else ""
        master_merged = parts[9] if len(parts) > 9 else ""
        status = parts[10] if len(parts) > 10 else ""
        description1 = parts[11] if len(parts) > 11 else ""

        extracted_data = {
            "Branch Name": branch_name,
            "Dev Done": dev_done,
            "Alpha Done": alpha_done,
            "Master Merged": master_merged,
            "Status": status,
            "Description":description1
        }
        data.update(extracted_data)
        write_data_to_sheet(data, start_row+i)

    return "Data Fetched successfully"

if __name__ == '__main__':
    app.run()
