## 📌 Prerequisites

### 💻 System requirement :

1. Any system with basic configuration.
2. Operating System : Any (Windows / Linux / Mac).

### 💿 Software requirement :

1. Updated browser
2. Python installed (If not download it [here](https://www.python.org/downloads/)).
3. Any text editor of your choice.

## 🎉 Setup

### Clone The Repository :

```
git clone https://github.com/NVombatYoutubeVideoFetcher.git
cd server
```

### .env File & Project Config :

1. Setup the .env file for MongoDB, Django & Google YouTube API functionality based on the .env.example file
2. For the YouTube API, First set up a project on Google Console, then generate API Keys

## 🔧 Installation

### Server :

Install python dependencies using [pip](https://pip.pypa.io/en/stable/)

```
$ pip install -r server/requirements.txt
```

Start the Django server

```
$ python3 manage.py runserver
```

### Redis :

First stop any pre-running Redis Server, then restart the Redis Server & check its status

```
$ sudo service redis-server stop
$ sudo service redis-server restart
$ sudo service redis-server status
```

Activate the Redis Server & test if its up and running

```
$ redis-server
$ redis-cli ping -> SHOULD RESPOND WITH PONG
```

Redis Server is now running in the background

### Celery :

Open two new terminal windows and go to the "server" directory

```
$ cd server
```

In one of the windows run celery worker so it is ready to receive tasks

```
$ celery -A core worker -l info
```

In the other window run celery beat so the task scheduler is ready for action

```
$ celery -A core beat -l info -s /path/to/file
```

Celery & Redis Have been used to create and run the task of fetching video data from the YouTube API repeatedly after a certain time interval

## 💥 Sending Requests

Use Postman to send GET requests to the server at specific URLs:
```
$ http://127.0.0.1:8000/api/fetchvids - GET request
$ http://127.0.0.1:8000/api/getdata - GET request
```
 - The first URL uses the YouTube API to fetch video data, and then stores it in the database
 - The second URL queries the database based on the parameters passed in the request to return a paginated response of the result of the request sent to the first URL
 - If the results for a query are not in the database, a request is made using the YouTube API and the results are fetched at that moment (Dynamic Searching)

### NOTE : THE API IS USED TO FETCH DATA FROM ALL EXISTING PAGES USING THE list() & list_next() FUNCTIONS.