# Finance Tracker Backend

A simple Flask API backend that helps retrieve data from MPESA PDFs sent to the email
The API also allows you to add goals and track budget expenditure.
Still currently a work in progress and drastic changes on how MPESA data is retrieved will occur

## Project Setup

Clone the repository into your machine using

```bash
$ git clone https://github.com/wesleymutwiri/mpesa-statement-retriever.git
```

Change directory into the folder downloaded

```bash
$ cd mpesa-statement-retriever
```

## File structure

**`api/`**

    - Contains the flask API for accessing endpoints and a way to make changes to data in the DB

**`scraper.py`**

    - Currently Hosts the functions for retrieving mpesa PDFs, unencrypting the PDF, and storing data to an sqlite database

**`pdfs/`**

    - Stores temporarily all PDFs retrieved from Gmail

**`unencrypted/`**

    - Stores unencrypted PDFs that have been unencrypted
