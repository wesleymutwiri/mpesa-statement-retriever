import camelot
import os
import subprocess
import pandas as pd

# ! Remove password from this file

headersICEA = [
    'Trans No',
    'Trans Date',
    'Description',
    'Deposit',
    'Interest',
    'Withholding Tax',
    'Balance'
]

def convertToCSV():
    tables = camelot.read_pdf("./unencrypted/ICEA-LION.pdf", flavor='stream' )
    temp = tables[2].df.copy()
    df = pd.DataFrame(columns=headersICEA)
    # print(temp, "This is the main with all the headers")
    temp.columns = headersICEA
    temp = temp.iloc[7:]
    print("\n\n\n Where transaction data starts \n\n\n")
    print(temp)
    for i in temp:
        print(i)
    # print(tables)
    # print(tables.n)
    # for i in range(tables.n):
        # print("There are {} tables".format(i))
        # df = pd.DataFrame(columns=headersICEA)
        # print(df[1])

def main():
    convertToCSV()


def removePasswordEncryption(password):
    subprocess.run(["qpdf", "--password={}".format(password),
                           "--decrypt", "statement.pdf", "unencrypted/{}".format("ICEA-LION.pdf")])


if __name__ == '__main__':
    main()
