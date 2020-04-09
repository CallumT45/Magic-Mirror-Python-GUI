#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from cogs import LoginsAndKeys as LaK

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('files/token.pickle'):
        with open('files/token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'files/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('files/token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId=LaK.api_keys["calendarId"], timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    eventList= []
    if not events:
        pass
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

        datetime_object = datetime.datetime.strptime(start, '%Y-%m-%dT%H:%M:%S+01:00').strftime('%H:%M %A %d')
        courseCode, courseName = event["summary"].split(":")
        eventList.append([datetime_object, courseName])  

    return eventList


