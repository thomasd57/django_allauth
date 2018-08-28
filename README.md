# Introduction
This is a repository to experiment with django allauth. 

# Initialization
```
manage.py migrate
manage.py init_db
manage.py runserver
```
You must have a secrets.env file setting the following variables.

```
DOMAIN_NAME=127.0.0.1
COMPANY_NAME=<your company name>
GITHUB_CLIENT_ID=
GITHUB_SECRET=
GOOGLE_CLIENT_ID=
GOOGLE_SECRET=
SPORTS_ENGINE_CLIENT_ID=
SPORTS_ENGINE_SECRET=
```

You can skip those you don't want to use.
