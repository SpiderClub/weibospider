#!/usr/bin/env bash

#### add admin user
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

#### add WeiboModel
django-admin.py startapp WeiboModel
#### make changes
python manage.py makemigrations WeiboModel
#### commit changes to db
python manage.py migrate WeiboModel

