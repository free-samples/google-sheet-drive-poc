import os.path
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',  # For file operations
    'https://www.googleapis.com/auth/drive.metadata.readonly'  # For folder operations
]

def get_credentials():
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

def create_folder(service, folder_name):
    try:
        # File metadata
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        # Create the folder
        file = service.files().create(
            body=file_metadata,
            fields='id, name, webViewLink'
        ).execute()

        print(f'Folder created successfully!')
        print(f'Folder ID: {file.get("id")}')
        print(f'Folder name: {file.get("name")}')
        print(f'Folder URL: {file.get("webViewLink")}')
        
        return file.get('id')

    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None

def main():
    try:
        # Get credentials
        creds = get_credentials()
        
        # Build the Drive service
        service = build('drive', 'v3', credentials=creds)
        
        # Create folder name with current date
        current_date = datetime.now()
        folder_name = f"Reports-{current_date.strftime('%Y-%b').upper()}"
        
        # Create the folder
        folder_id = create_folder(service, folder_name)
        
        if folder_id:
            print(f'You can now use this folder ID in other scripts: {folder_id}')
        
    except Exception as e:
        print(f'An error occurred: {str(e)}')

if __name__ == '__main__':
    main()
