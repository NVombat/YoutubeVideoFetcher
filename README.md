## 📌 Prerequisites

### 💻 System requirement :

1. Any system with basic configuration.
2. Operating System : Any (Windows / Linux / Mac).

### 💿 Software requirement :

1. Updated browser
2. Python installed (If not download it [here](https://www.python.org/downloads/)).
3. Any text editor of your choice.

## Installation 🔧

### Server

Install python dependencies

```
$ pip install -r server/requirements.txt
```

Setup the .env file for Database & Google YouTube API functionality
NOTE: For the YouTube API, First you will need to set up a project in your Google Console and then get API Keys

Start the Django server

```
$ python3 manage.py runserver
```

## 💥 Sending Requests

Use Postman to send GET requests to the server at specific URLs:
```
http://127.0.0.1:8000/api/fetchvids - GET request
http://127.0.0.1:8000/api/getdata - GET request
```
The first URL uses the YouTube API to fetch video data, and then stores it in the database
The second URL queries the database based on the parameters passed in the request to return a paginated response of the result of the request sent to the first URL