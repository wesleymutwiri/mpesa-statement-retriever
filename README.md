# Finance Tracker Backend

A simple Flask API backend that helps retrieve data from MPESA PDFs sent to the email
The API also allows you to add goals and track budget expenditure.
Still currently a work in progress and drastic changes on how MPESA data is retrieved will occur

## Table of Contents

- [Finance Tracker Backend](#finance-tracker-backend)
  - [Table of Contents](#table-of-contents)
  - [Project Setup](#project-setup)
  - [File structure](#file-structure)
  - [REST API](#rest-api)
    - [Get list of Users](#get-list-of-users)
      - [Get list of Users Request](#get-list-of-users-request)
      - [Response](#response)
    - [Create a new Goal](#create-a-new-goal)
      - [Create Goal Request](#create-goal-request)
      - [Create Goal Response](#create-goal-response)
    - [Get a specific Goal](#get-a-specific-goal)
      - [Get a specific Goal Request](#get-a-specific-goal-request)
      - [Get a specific Goal Response](#get-a-specific-goal-response)
    - [Get a non-existent goal](#get-a-non-existent-goal)
      - [Get a non-existent goal Request](#get-a-non-existent-goal-request)
      - [Get a non-existent goal Response](#get-a-non-existent-goal-response)
  - [Thought Process](#thought-process)
  - [Features](#features)
  - [Process](#process)

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

## REST API

The REST API to the finance tracker app is described below.

### Get list of Users

#### Get list of Users Request

`GET /goals`

    curl -i -H 'Accept: application/json' http://localhost:5000/goals

#### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    []

### Create a new Goal

#### Create Goal Request

`POST /goals`

    curl -i -H 'Accept: application/json' --data '{"current_price": 2000,"description": "description here","due_date": "2021-11-08","name": "changed","price_required": 30000}' http://localhost:5000/goals

#### Create Goal Response

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

### Get a specific Goal

#### Get a specific Goal Request

`GET /goals/id`

    curl -i -H 'Accept: application/json' http://localhost:8080/goals/1

#### Get a specific Goal Response

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

### Get a non-existent goal

#### Get a non-existent goal Request

`GET /goals/id`

    curl -i -H 'Accept: application/json' http://localhost:8080/goals/9999

#### Get a non-existent goal Response

    HTTP/1.1 404 Not Found
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 404 Not Found
    Connection: close
    Content-Type: application/json
    Content-Length: 35

    {"error":"record not found"}

## Thought Process

This project is meant to get data from various banks and sources of revenue via email and then do a portfolio evaluation of the same. The processing part of the application will require us to sync all of the debit and credit facilities. This will be done during the processing of the PDFs.

We would also require to know our net-worth, so I'll need to get data from the stock exchange and the Kenyan stock market through a scraper and combine that data to do a day after day analysis of how much money I'm making, daily, weekly, or yearly. This data will be stored daily at a specified time and then added to an SQLite database. The SQLite database should be updated every month at a specified date, highly likely 5th of every month. This will require an update script that is a Linux cronjob. The application will be hosted somewhere locally, not sure where and be linked to a separate project that analyses and predicts whether we're financially secure or not.

This app needs to be able to get percentage interests and compound interest over years, showing how long it would take me to get financially secure/independent. It should also track different crypto and get data on my current crypto portfolio based on my freqtrade trades. A snapshot everyday of how I have progressed needs to be added. A simple graph/bar/line/candle chart should be able to show how different investing strategies have performed over a certain number of days, years and weeks.

## Features

- [ ] Get Financial PDFs from my group Chama
- [ ] Get Financial PDFs from my Standard Chartered bank from protonmail
- [ ] Get Financial PDFs from my mpesa
- [ ] Get Financial PDFs from my Equity account
- [ ] Get current snapshots of Stock (Both internationally and Locally)
- [ ] Get Crypto data
- [ ] Calculate compounding interest over a certain amount of time
- [ ] Calculate current trajectory over a number of years (Get the financial portfolio after a certain period of time if investing continues in the same rate every month)
  - [ ] Calculate how long it would take someone to be financially secure with the investments listed
  - [ ] Determine better performing asset classes
  - [ ] Showcase the financial portfolio allocations and how much has been invested vs the amount of money that it has returned
- [ ] Add different calculators for different loans and interest rates
  - [ ] Add a mortgage calculator
  - [ ] Add a Sacco loan calculator

## Process

- [ ] Create login page
- [ ] Create register page
- [ ] Add authentication and token authorisation on the back-end
- [ ] Create dashboard page that includes a menu to different pages such as
  - [ ] Calculators for different types of loans
  - [ ] Current stock and crypto prices
  - [ ] Detailed search analysis for yearly, weekly and monthly transaction data
  - [ ] Page that analyses amount of money spent on different categories of payments
- [ ] Add functions for retrieving and parsing PDFs from group chama
- [ ] Add function for retrieving and parsing PDFs from standard chartered (Resend emails from protonmail to gmail in order to receive the emails at the same time as the MPesa statements)
- [ ] Add function for retrieving and parsing PDFs from equity bank
- [ ] Get and display stock and crypto prices from open source API
- [ ] Write function to calculate profit/loss dependant on whether the stock prices have risen or fallen within the time period specified
- [ ] Write a function to calculate compounding interest based on the percentage provided online
- [ ] Write a function to calculate loan and interest rates
- [ ] Write a function to calculate the current financial portfolio and trajectory on when financial independence will occur
- [ ] Add categorization in order to calculate personal and group financial portfolios
