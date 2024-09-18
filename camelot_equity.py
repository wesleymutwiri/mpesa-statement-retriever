import camelot
import os
import subprocess
import pandas as pd

# ! Remove password from this file


# TODO Add all headers into special file in order to be able to just choose from one of the selections afterwards
headersEquity = [
    'Date',
    'Value Particulars',
    'Money Out',
    'Money In',
    'Balance'
]


# TODO change convertTOCSV function to include swapping headers and changing how the input is saved
# TODO Add functions that allow each row to be saved specifically in a certain order depending on the bank used
def convertToCSV():
    tables = camelot.read_pdf("./unencrypted/equity.pdf", flavor='stream' )
    temp = tables[0].df.copy()
    # df = pd.DataFrame(columns=headersEquity)
    # print(df)
    print(temp, "\n\n\n This is the main with all the headers \n \n \n")
    # temp.columns = headersEquity
    print("\n\n\n Where transaction data starts \n\n\n")
    # print(temp[1:-1])
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
    # removePasswordEncryption()

# TODO add file and destination inputs in order to make a more reusable function
def removePasswordEncryption(password):
    subprocess.run(["qpdf", "--password={}".format(password),
                           "--decrypt", "statement.pdf", "unencrypted/{}".format("equity.pdf")])


if __name__ == '__main__':
    main()
