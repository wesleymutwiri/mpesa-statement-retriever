# Finance Tracker Backend

A simple Flask API backend that helps retrieve data from MPESA PDFs sent to the email
The API also allows you to add goals and track budget expenditure.
Still currently a work in progress and drastic changes on how MPESA data is retrieved will occur

## Project Setup

Clone the repository into your machine using

```bash
git clone https://github.com/wesleymutwiri/mpesa-statement-retriever.git
```

Change directory into the folder downloaded

```bash
cd mpesa-statement-retriever
```

In order to use the scraper, you'll need to activate the Gmail API and place the `token.json` file in the root path of this project. Once the scraper is run it will prompt the user to sign in and allow access to their gmail account.

You can use any python virtual environment but personally I prefer to use [pipenv]() which you'll need to install on your machine and activate

```bash
pipenv shell
pipenv install
```

To run the scraper, afterwards, you simply run the python file `scraper.py` which contains code for scraping the mpesa PDFs from your gmail account.

```bash
python3 scraper.py
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

# REST API

The REST API to the finance tracker app is described below.

## Get list of Users

### Request

`GET /goals`

    curl -i -H 'Accept: application/json' http://localhost:5000/goals

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    []

## Create a new Goal

### Request

`POST /goals`

    curl -i -H 'Accept: application/json' --data '{"current_price": 2000,"description": "description here","due_date": "2021-11-08","name": "changed","price_required": 30000}' http://localhost:5000/goals

### Response

    HTTP/1.1 201 Created
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 201 Created
    Connection: close
    Content-Type: application/json
    Location: /thing/1
    Content-Length: 36

    {
        "result": {
            "current_price": 2000,
            "description": "some new description here",
            "due_date": "2021-11-08",
            "id": 3,
            "is_completed": false,
            "name": "chaasdfsdnged",
            "price_required": 30000,
            "timestamp": "2021-12-14T09:40:55.681043"
        }
    }

## Get a specific Goal

### Request

`GET /goals/id`

    curl -i -H 'Accept: application/json' http://localhost:8080/goals/1

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 36

    {
        "id":1,
        "username":"wes",
        "email":"wes@gmail.com",
        "created_at":"2020-11-10T20:57:31.763849+03:00",
        "updated_at":"2020-11-10T20:57:31.763849+03:00"
    }

## Get a non-existent goal

### Request

`GET /goals/id`

    curl -i -H 'Accept: application/json' http://localhost:8080/goals/9999

### Response

    HTTP/1.1 404 Not Found
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 404 Not Found
    Connection: close
    Content-Type: application/json
    Content-Length: 35

    {"error":"record not found"}
