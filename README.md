# Share Eats
## Project completed by : 
###Kweku Amankwah-Poku - x2019ekw@stfx.ca
###Vineeth Parsi - x2020ezg@stfx.ca
###Shubham Poriya - x2020fem@stfx.ca
###Michelle Vava - x2018uxm@stfx.ca
###Vijay Pereira - x2020fyf@stfx.ca

## About ##

We have developed a web application called Share Eats which allows the Antigonish community to buy and sell food items.

## Prerequisites ##

- Python 2.7, 3.4 recommended
- pip
- PyCharm/VS Code
- Postgres
- virtualenv (virtualenvwrapper is recommended for use during development)
- 
## Features

- Django 3.0+
- HTTPS and other security related settings on Staging and Production.
- Procfile for running gunicorn with New Relic's Python agent.
- Dockerfile and Docker-compose.yml
- PostgreSQL database support with psycopg2.

Migrations:

- Django built-in migrations

## Setup

The first thing to do is to clone the repository:


```sh
$ git clone https://groupf1-admin@bitbucket.org/groupf1/shareeats.git

```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ cd shareeats
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:7000/`.

## Deployment

It is possible to deploy to Heroku or to your own server.

### Heroku

```bash
$ heroku create
$ heroku addons:add heroku-postgresql:hobby-dev
$ heroku pg:promote DATABASE_URL
$ heroku config:set ENVIRONMENT=PRODUCTION
$ heroku config:set DJANGO_SECRET_KEY=`./manage.py generate_secret_key`
```




## Docker images

Share Ears uses images for CI runs.The image is python based and contain python3, pip and some support
packages. The images are published to  [docker hub](https://hub.docker.com/repository/docker/mimivava26/share-eats).

The images are built in CI (from main branches only) and also updated every day via schedules.

You can pull the image from docker hub using the following prompt onto your local :
```sh
docker pull mimivava26/share-eats: latest
```

Once successful then you can run the image :
```sh
docker run --publish 7000:7000 shareeats-dev
```

On your browser run enter this URL :
```sh
localhost:7000