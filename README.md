# Data Center

<Your Project Description>

## About

Developed an API to fetch latest videos sorted in reverse chronological
order of their publishing date-time from YouTube for a given tag/search
query in a paginated response. Details are as follows:

1. Server calls the YouTube API continuously in background (async) with the interval of 30 seconds for fetching the latest videos for a predefined search query (Cricket) and stores the data of videos in a database.
2. Search query can be changed from django admin. `Django Admin > Config > SEARCH_QUERY`
3. Time interval of the periodic task (async task) can also be changed from Django Admin.
    `Django Admin > Periodic tasks > sync youtube videos`
4. Due to a restricted resources and youtube API quota, this project is configured to call and store first four pages of data having 50 videos each. Hence details about 200 videos will be saved in single task execution by default. However we can configure data of how many pages to be saved using Django admin. `Django Admin > Config > EPOCHS`
5. We send `publishedAt` of the latest video detail observed as `publishedAfter` in youtube search API to get latest results. We would not be knowing this latest `publishedAt` for the very first call, hence we pass a default datetime `2021-06-02T16:42:19Z`. This is also configurable from django admin. `Django Admin > Config > DEFAULT_LATEST_VIDEO_DATETIME`
6. Developed a GET API which returns the stored video data in a paginated response sorted in descending order of published datetime. Can be accessed at `<host>:<port>/api/youtube/api/`
7. Above API also works as search API to search the stored videos using their title and description. Add `search` in query params to use this functionality. For eg. `search=Virat Kohli`. Optimised search api, so that it's able to search videos containing partial match for the search query in either video title or description.
8. Dockerized the project.
9. Developed a dashboard to view the stored videos with filters and sorting options. Can be accessed through Django Admin. `Django Admin > Videos`
10. Can also see request and response contracts at `<host>:<port>/api/youtube/swagger/`
11. Pass `limit` and `offset` in query params to get paginated response.


## Repo Setup

1. Set Environment Values

    * Copy the .env_template to .env
    * Fill the values of .env as required


### Docker Setup and Run

`docker-compose up --build`

Then use `localhost:8008/api/youtube/api` from postman to check the APIs.

If you want fine tuned run, read next section

### Setup steps

1. Get the repo

    * Visit the repo and fork it
    * Clone the repo by using `git clone <repo/path>`
    * `cd youtubeSearch`

2. Install requirements and pre-commit hooks

    1. Run the following command.

        `make install`


### Manual Setup and Run

1. Install virtualenv, pre-commit hook, requirements and migration.

    `make install`

2. To Runserver Locally (Not for Prod or staging):

    `python manage.py runserver 8000`

    Or

    `make server`

    The above command will run the server on port 8000

3. To Run Celery worker on local

    `celery -A data_center.celery_app worker -B`


4. To Run Celery beat on local

    `celery beat -A data_center.celery_app -l info`


## Make

```
Usage: make <target>

Targets:
help           Show this help message
clean_pyc      Clean all *.pyc files
update         Update all necessary requirements and migrate
install        Install all necessary requirements
migrations     Make migrations
migrate        Apply migration files
test           Run tests
test-cov       Run tests with coverage
report         Coverage report
build          Build
pre_commit     Pre commit
collectstatic  Collects static files
server         Run python server only
admin          Creates Administrator account
version        Print version information
```
