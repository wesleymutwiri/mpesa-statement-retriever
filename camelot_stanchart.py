import camelot
import os
import subprocess
import pandas as pd

# ! Remove password from this file
headersStanchart = [
    'Entry Date',
    'Value Date',
    'Description',
    'Deposit',
    'Withdrawal',
    'Balance'
]

def convertToCSV():
    tables = camelot.read_pdf("./unencrypted/stanchart.pdf", flavor='stream', pages='all')
    for i in range(tables.n):
        temp = tables[i].df.copy()
        print(temp)
    # df = pd.DataFrame(columns=headersStanchart)
    # print(temp, "This is the main with all the headers")
    # temp.columns = headersStanchart
    # temp = temp.iloc[7:]
    # print("\n\n\n Where transaction data starts \n\n\n")
    # print(temp)
    # for i in temp:
    #     print(i)
    # print(tables)
    # print(tables.n)
    # for i in range(tables.n):
        # print("There are {} tables".format(i))
        # df = pd.DataFrame(columns=headersICEA)
        # print(df[1])

def main():
    convertToCSV()
    # removePasswordEncryption("")


def removePasswordEncryption(password):
    subprocess.run(["qpdf", "--password={}".format(password),
                           "--decrypt", "statement.pdf", "unencrypted/{}".format("stanchart.pdf")])


if __name__ == '__main__':
    main()
