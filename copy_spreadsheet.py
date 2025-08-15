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

def copy_spreadsheet(creds, source_spreadsheet_id, new_title):
    try:
        service = build('sheets', 'v4', credentials=creds)
        
        # Get the source spreadsheet to get its parent folder
        source = service.spreadsheets().get(
            spreadsheetId=source_spreadsheet_id).execute()
        
        # Create the copy request
        drive_service = build('drive', 'v3', credentials=creds)
        
        # Create copy of the spreadsheet in the specified folder
        copy_request = drive_service.files().copy(
            fileId=source_spreadsheet_id,
            body={
                'name': new_title,
                'parents': ['1Qr926OL2w3gg3aQPQb8JAFux2SaXx4_E']  # Specify the destination folder
            }
        )
        copied_file = copy_request.execute()
        
        print(f'Spreadsheet copied successfully!')
        print(f'New spreadsheet ID: {copied_file["id"]}')
        print(f'New spreadsheet name: {copied_file["name"]}')
        print(f'Copied to folder: 1Qr926OL2w3gg3aQPQb8JAFux2SaXx4_E')
        
        return copied_file["id"]
        
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None

def main():
    try:
        # Get the source spreadsheet ID from user
        source_spreadsheet_id = "16otco8398JUg-ghCRIliEYoYf8rm-GtKidgMOjxjiFs"
        new_title = "Report - " + datetime.now().strftime("%Y-%b")
                
        # Get Google Sheets credentials
        creds = get_google_sheets_credentials()
        
        # Copy the spreadsheet
        copy_spreadsheet(creds, source_spreadsheet_id, new_title)
        
    except Exception as e:
        print(f'An error occurred: {str(e)}')

if __name__ == '__main__':
    main()
