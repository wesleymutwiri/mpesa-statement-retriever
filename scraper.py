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
import subprocess
import camelot
import sqlite3
import csv
import pandas as pd
from sqlite3 import Error
import datetime
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """

    # for result in results:
    #     print(result['id'])

    # convertPDFToHTML(filename)
    # removePasswordEncryption()
    # for filename in os.listdir("unencrypted"):
    #     if filename.endswith(".pdf"):
    #         convertPDFToCSV("unencrypted/{}".format(filename),
    #                         os.path.splitext(filename)[0]+".csv")
    # create_connection("database.db")

    headers = [
        'Receipt No.',
        'Completion Time',
        'Details',
        'Transaction',
        'Paid In',
        'Withdrawn',
        'Balance'
    ]

    totalCostHeaders = [
        'Transaction Type',
        'Paid In',
        'Paid Out'
    ]

    conn = create_connection("database.db")
    for filename in os.listdir("unencrypted"):
        if filename.endswith(".pdf"):
            dateRetrieval = filename.split("_")
            dateFrom = datetime.datetime.strptime(dateRetrieval[2], "%Y%m%d")
            dateTo = datetime.datetime.strptime(dateRetrieval[4], "%Y%m%d")
            # print(dateFrom, "-", dateTo)
            tables = camelot.read_pdf(
                "unencrypted/{}".format(filename), pages='all', line_size_scaling=16.93)
            for i in range(tables.n):
                df = pd.DataFrame(columns=headers)
                smallDf = pd.DataFrame(columns=totalCostHeaders)
                # print(df)
                # all_tables = tables[i].df
                # if tables[i].shape[1] == 7:
                #     temp = tables[i].df.copy()
                #     temp.columns = headers
                #     temp = temp.iloc[1:]
                #     saved_table = pd.concat([df, temp], sort=False)
                #     saved_table.to_sql(name="Transactions", con=conn,
                #                        if_exists="append", index=False)
                #     print(saved_table)
                # print("Seven columned")
                if tables[i].shape[1] == 3:
                    temp = tables[i].df.copy()
                    temp.columns = totalCostHeaders
                    temp = temp.iloc[2:]
                    temp["dateFrom"] = dateFrom
                    temp["dateTo"] = dateTo
                    saved_table = pd.concat([smallDf, temp], sort=False)
                    saved_table.to_sql(name="TotalsTrial", con=conn,
                                       if_exists='append', index=False, method='multi')

                    print(saved_table)


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn


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

    # Call the Gmail API
    results = service.users().messages().list(
        userId='me', q="from:m-pesastatements@safaricom.co.ke").execute()
    # for i in results['messages']:
    #     print(i)
    # labels = results.get('labels', [])

    # if not results:
    #     print('No emails found.')
    # else:
    #     print('Emails:', results)
    # for i in results:

    for result in results['messages']:
        # trial = json.loads(result)
        print(result['id'])
        try:
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
                    path = part['filename']

                    f = open(path, 'wb')
                    f.write(file_data)
                    f.close()

        except errors.HttpError as error:
            print('An error occurred: %s', error)


# def convertPDFToHTML(filename):
    # for filename in os.listdir("unencrypted"):
    #     if filename.endswith(".pdf"):
    # convertPDFToCSV("unencrypted/{}".format(filename),
    #                 os.path.splitext(filename)[0]+".csv")


def removePasswordEncryption(password):
    try:
        os.mkdir("tables")
        os.mkdir("unencrypted")
    except OSError as error:
        print(error)
    for filename in os.listdir("pdfs"):
        if filename.endswith(".pdf"):
            subprocess.run(["qpdf", "--password={}".format(password),
                           "--decrypt", "pdfs/{}".format(filename), "unencrypted/{}".format(filename)])


def convertPDFToCSV(pdf, output):
    tables = camelot.read_pdf(pdf, pages="all", flavor='stream')
    tables.export("tables/{}".format(output), f="csv", compress=False)


if __name__ == '__main__':
    main()
