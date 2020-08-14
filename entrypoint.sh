#!/bin/bash
mv /usr/lib/python3.7/site-packages/pip/_internal/index /usr/lib/python3.7/site-packages/pip/_internal/index_bak
pip3 install django djangorestframework pdbpp
python3 manage.py makemigrations && python3 manage.py migrate
python3 manage.py runserver
mkdir -p /etc/uwsgi/apps-available /etc/uwsgi/apps-enabled
cp /code/users/usermanage/usermanage.ini /etc/uwsgi/apps-available/usermanage.ini
cd /run/
mkdir -p uwsgi
cd /var/log
mkdir -p uwsgi
ln -sf /etc/uwsgi/apps-available/usermanage.ini /etc/uwsgi/apps-enabled/
cp /code/users/usermanage/uwsgi.service /etc/systemd/system/uwsgi.service
systemctl start uwsgi
# nginix stuff
cp /code/users/usermanage/usermanage.conf /etc/nginx/sites-available/usermanage
ln -s /etc/nginx/sites-available/usermanage /etc/nginx/sites-enabled/
systemctl restart uwsgi
service nginx start