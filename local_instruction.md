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

In settings.py, on line 27 replace/update the secret key with the one you generated in the previous step

```bash
SECRET_KEY = env("DJANGO_SECRET_KEY")
```
to
```bash
SECRET_KEY = env("DJANGO_SECRET_KEY", default="the new secret key you just generated")
```

In line 94 to 97, since we are not using a postgres db from heroku, comment out the db, and use a simple sqlite db instead, should look like below

```bash
# DATABASES = {
#     "default": env.dj_db_url("DATABASE_URL",
#     default="postgres://postgres@db/postgres")
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / "db.sqlite3",
    }
}
```

At the very bottom of the file, make sure O is False and everything below it is commented out, see below

```bash
SECURE_SSL_REDIRECT = False
# SECURE_HSTS_SECONDS = env.int("DJANGO_SECURE_HSTS_SECONDS", default=2592000)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool(
#     "DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", default=False
# )
# SECURE_HSTS_PRELOAD = env.bool("DJANGO_SECURE_HSTS_PRELOAD", default=False)
# SESSION_COOKIE_SECURE = env.bool("DJANGO_SESSION_COOKIE_SECURE", default=False)
# CSRF_COOKIE_SECURE = env.bool("DJANGO_CSRF_COOKIE_SECURE", default=False)
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# USE_X_FORWARDED_PORT = False
```

## Post db prep work

Run a migrate
```bash
python manage.py migrate
```

Collect static (I don't even think you need to do this but habits)
```bash
python manage.py collectstatic
```

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

NOTE, the admin url is not /admin but /look-away-pls