#!/usr/bin/env bash

clear;

echo 'Deleting pyc files if there are any...'
find . -name "*.pyc" | xargs rm

echo

echo 'Killing current Gunicorn instances if there are any...'
kill -9 `ps aux | grep gunicorn | awk '{print $2}'`

echo

echo 'Django & OpenCV at http://localhost:8000'
gunicorn django_camera.wsgi:application --bind localhost:8000 --daemon --workers 8