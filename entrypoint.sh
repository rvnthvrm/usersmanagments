#!/bin/bash
mv /usr/lib/python3.7/site-packages/pip/_internal/index /usr/lib/python3.7/site-packages/pip/_internal/index_bak
pip3 install django djangorestframework pdbpp
python3 manage.py makemigrations && python3 manage.py migrate &&
uwsgi --socket 0.0.0.0:8000 --protocol=http --chdir=/code/users -w users.wsgi