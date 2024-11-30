# Reason for this instruction set

Originally this project was made and deployed to heroku, but since I do not have it active anymore, I quickly made step by step instructions on how to prep this to run locally to test and look around in a dev enviroment

## Prerequisites

I believe one of the lib in requirements.txt(psycopg2-binary) only works with Python 3.9, so you will need to download that specific version and create a venv with it (or however you would prefer to use a specific version)

To init the venv, and activate

```bash
/Location/Of/Python/Python39/python -m venv .venv
source .venv/Scripts/activate
```

Ensure you are using Python 3.9

```bash
python --version
```

Install the necessary requirements

```bash
python -m pip install -r requirements.txt
```

Generate new secret token (NEVER do this in prod), save for next step

```bash
django-admin shell
```
```bash
>>> from django.core.management.utils import get_random_secret_key 
>>> get_random_secret_key()
```

## Prep settings.py

Change the `.env-example` filename to `.env`

In `.env`, on line 1 replace/update the secret key with the one you generated in the previous step

```bash
DJANGO_SECRET_KEY="PASTE_DJANGO_SECRET_KEY_HERE"
```

## Post db prep work

Run a migrate
```bash
python manage.py migrate
```

Collect static (I don't even think you need to do this since we local but habits)
```bash
python manage.py collectstatic
```

Run the backfill for data
```bash
python manage.py backfill_dummy
```

(Optional)
Create a super user
```bash
python manage.py createsuperuser
```

Run the server (without 8080 it will default to port 8000, on my local machine I had to run with 8080)
```bash
python manage.py runserver 8080
```

From here you can login with the super user you created

There won't be any images since the db is fresh, but you can go on the admin panel to add images, users, comments etc

NOTE, the admin url path is not `/admin` but `/look-away-pls`