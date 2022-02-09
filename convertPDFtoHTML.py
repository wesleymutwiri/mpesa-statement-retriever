import sqlite3
import pandas as pd
from sqlite3 import Error
import datetime
import os
import os
import subprocess
import camelot


def main():
    convertPDFToDatabase()


def convertPDFToDatabase():
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
                all_tables = tables[i].df
                if tables[i].shape[1] == 7:
                    temp = tables[i].df.copy()
                    temp.columns = headers
                    temp = temp.iloc[1:]
                    saved_table = pd.concat([df, temp], sort=False)
                    saved_table.to_sql(name="Transactions", con=conn,
                                       if_exists="append", index=False)
                    print(saved_table)
                print("Seven columned")
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


# If anyone requires CSV format instead of an API
def convertPDFToCSV(pdf, output):
    tables = camelot.read_pdf(pdf, pages="all", flavor='stream')
    tables.export("tables/{}".format(output), f="csv", compress=False)


if __name__ == '__main__':
    main()
