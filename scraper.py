from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
from apiclient import errors
import json
# import pikepdf
# import tabula
import os
from sqlite3 import Error
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """
    Get all files from your GMail sent by a specific user
    """
    getAttachmentsFromEmail()


def getAttachmentsFromEmail():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)
    """
        Call the Gmail API specifying that the email address 
        is from mpesa-statememts@safaricom.co.ke 
    """
    results = service.users().messages().list(
        userId='me', q="from:m-pesastatements@safaricom.co.ke").execute()

    for result in results['messages']:
        try:
            # Get all messages from the API where 
            # the userID is the currently logged in user
            message = service.users().messages().get(
                userId='me', id=result['id']).execute()

            for part in message['payload']['parts']:
                if part['filename']:
                    if 'data' in part['body']:
                        data = part['body']['data']
                    else:
                        att_id = part['body']['attachmentId']
                        att = service.users().messages().attachments().get(
                            userId='me', messageId=result['id'], id=att_id).execute()
                        data = att['data']
                    file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
                    path = "pdfs/" + part['filename']

                    f = open(path, 'wb')
                    """
                    If statement check to confirm if the PDF has already been 
                    downloaded or save the file if it doesn't exist currently
                    """
                    if os.path.exists("pdfs/" + part['filename']):
                        # print(part['filename'])
                        continue
                    else:
                        f.write(file_data)
                        f.close()

        except errors.HttpError as error:
            print('An error occurred: %s', error)


if __name__ == '__main__':
    main()
