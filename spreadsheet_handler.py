from datetime import datetime
import os.path
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'  # Added drive scope for copying files
]

def get_google_sheets_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens
    if os.path.exists('credentials/token.pickle'):
        with open('credentials/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('credentials/token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def clear_column_c(creds, spreadsheet_id):
    try:
        service = build('sheets', 'v4', credentials=creds)
        
        # First, let's get the range of data in the sheet to know how many rows to clear
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        properties = sheet_metadata.get('sheets')[0].get('properties')
        row_count = properties.get('gridProperties').get('rowCount')
        
        # Create the range for column C (from C1 to the last row)
        range_name = 'Sheet1!C:C'
        
        # Create the clear request
        clear_request = service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            body={}
        )
        
        # Execute the request
        response = clear_request.execute()
        
        print('Column C has been cleared successfully!')
        print(f'Cleared range: {response.get("clearedRange")}')
        
    except Exception as e:
        print(f'An error occurred: {str(e)}')

def main():
    try:
        # Spreadsheet ID
        spreadsheet_id = "1h54vHwSRZ8UZ0gprV0Qs2imdCFxZNqmcQHMSXs0T7f8"
        
        # Get Google Sheets credentials
        creds = get_google_sheets_credentials()
        
        # Clear column C
        clear_column_c(creds, spreadsheet_id)
        
    except Exception as e:
        print(f'An error occurred: {str(e)}')

if __name__ == '__main__':
    main()
