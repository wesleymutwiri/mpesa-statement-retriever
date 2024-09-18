mport sqlite3
import pandas as pd
from sqlite3 import Error
import datetime
import os
import os
import subprocess
import camelot


headersICEA = [
    'Transaction No.',
    'Trans Date',
    'Description',
    'Deposit',
    'Interest',
    'Withdrawal',
    'Withholding Tax',
    'Balance'
]


class FinancialPDF:
    """
    FinancialPDF is a class that allows for the grouping of all financial statements sent by banks as a PDF.
    The banks documents are downloaded, unencrypted and then use camelot - the python package to read and extract data
    from the financial statements. This data will then be stored elsewhere in order to be retrieved later on when conducting analysis.

    headers = The headers on the PDF file, it is required for camelot to be able to parse the data correctly
    filepath = Full path link to the unencrypted PDF file that needs to be parsed by camelot
    organization = The organization where the financial statement has been retrieved from e.g M-pesa, Standard Chartered, NCBA etc
    password = Provide the password in case the financial statement has been encrypted and cannot be retrieved

    """

    def __init__(self, headers, filepath, organization, password):
        self.headers = headers
        self.file = filepath
        self.organization = organization
        self.password = password


    def convertToCSV(self):
        tables = camelot.read_pdf(self.file, pages='all', flavor='stream')
        print(tables)
