import pandas as pd
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

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

def create_spreadsheet(creds, title):
    service = build('sheets', 'v4', credentials=creds)
    spreadsheet = {
        'properties': {
            'title': title
        }
    }
    spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                              fields='spreadsheetId').execute()
    return spreadsheet.get('spreadsheetId')

def update_values(creds, spreadsheet_id, range_name, values):
    service = build('sheets', 'v4', credentials=creds)
    body = {
        'values': values
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='RAW', body=body).execute()
    return result

def main():
    # Read the CSV file
    try:
        df = pd.read_csv('sample.csv')
        # Get the first column as a list
        first_column_name = df.columns[0]
        first_column_data = df[first_column_name].tolist()
        # Add the header to the data
        data = [[first_column_name]] + [[str(item)] for item in first_column_data]
        
        # Get Google Sheets credentials
        creds = get_google_sheets_credentials()
        
        # Create a new spreadsheet
        spreadsheet_id = create_spreadsheet(creds, 'CSV Data Import')
        print(f'Created spreadsheet with ID: {spreadsheet_id}')
        
        # Update the spreadsheet with our data
        range_name = 'A1:A' + str(len(data))
        update_values(creds, spreadsheet_id, range_name, data)
        print('Data successfully imported to Google Sheets!')
        
    except Exception as e:
        print(f'An error occurred: {str(e)}')

if __name__ == '__main__':
    main()