# CSV to Google Sheets POC

This is a simple Python script that reads data from a CSV file and creates a Google Spreadsheet with the contents of the first column.

## Setup Instructions

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API for your project
4. Create credentials (OAuth 2.0 Client ID):
   - Go to APIs & Services > Credentials
   - Click "Create Credentials" and select "OAuth client ID"
   - Choose "Desktop app" as the application type
   - Download the credentials
5. Save the downloaded credentials file as `credentials.json` in the `credentials` directory

## Requirements

- Python 3.x
- pandas
- google-api-python-client
- google-auth-httplib2
- google-auth-oauthlib

The required Python packages will be installed automatically when you run the script in the virtual environment.

## Usage

1. Make sure you have your CSV file ready (a sample.csv is provided)
2. Place your `credentials.json` file in the `credentials` directory
3. Run the script:
   ```bash
   python csv_to_sheets.py
   ```

The first time you run the script, it will open a browser window asking you to authorize the application. After authorization, it will create a new Google Spreadsheet with the data from the first column of your CSV file.

## Notes

- The script will create a new spreadsheet each time it runs
- Only the first column from the CSV file will be imported
- The spreadsheet will be named "CSV Data Import"
