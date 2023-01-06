**JIRA Issue Tracker**

This script is a simple issue tracker that reads ticket numbers from a Google Sheets document, fetches data for those tickets from a JIRA instance, and writes the data back to the sheet. It uses the Flask framework to expose a simple endpoint for running the script.

**Requirements**

This script requires the following packages:

-Flask
-google-auth
-google-auth-oauthlib
-google-auth-httplib2
-google-api-python-client
-requests
-python-dotenv

**Usage**
1. Clone the repository and navigate to the directory.
2. Create a .env file and set the following environment variables:
    -CLIENT_ID: The client ID for a Google API project.
    -CLIENT_SECRET: The client secret for a Google API project.
    -REFRESH_TOKEN: The refresh token for a Google API project.
    -TOKEN_URI: The token URI for a Google API project.
    -USER_AGENT: A user agent string for the Google API client.
    -API_ENDPOINT: The base URL for the JIRA instance, including the API path.
    -JIRA_USERNAME: The username for the JIRA instance.
    -PASSWORD: The password for the JIRA instance.
    -SPREADSHEET_ID: The ID of the Google Sheets document to read from and write to.
    -SHEET_NAME: The name of the sheet in the document to read from and write to.
3. Install the required packages using pip install -r requirements.txt.
4. Run the script using flask run.
5. Access the endpoint at http://localhost:5000/test.

**Notes**

-The script expects the sheet to have the following columns: "Name", "Ticket Number", "Branch Name", "Dev Done", "Alpha Done", "Master Merged", "Status", "Description".
-The script starts reading from the second row of the sheet (row 2).
-The script expects ticket numbers to be in the "Ticket Number" column (column B).
-The script expects the ticket data to be in the following format in the "Description" column (column H): | Branch Name | Dev Done | Alpha Done | Master Merged | Status |. If any of these fields are not present, they will be left blank in the sheet.