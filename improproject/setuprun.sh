#!/bin/bash
yarn install
pipenv install --dev
pipenv run python3 manage.py migrate

redis-server --daemonize yes
echo CONFIG SET protected-mode no | redis-cli
pipenv run python manage.py runserver 192.168.178.22:8000 &
sleep 5
yarn serve
