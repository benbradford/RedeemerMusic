#!/bin/bash
sudo mkdir -p /var/www/flask/redeemer_music
sudo cp -r ../* /var/www/flask/redeemer_music
sudo cp flask.service /lib/systemd/system/flask.service
systemctl enable flask
cp start.sh /var/www/flask/redeemer_music/start.sh
chmod +x /var/www/flask/redeemer_music/start.sh
cd /var/www/flask/redeemer_music
sudo virtualenv env
source env/bin/activate
sudo pip install -r requirements.txt
deactivate
rm /etc/nginx/sites-enabled/default
cp reverse-proxy.conf /etc/nginx/sites-enabled/nginx.conf
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/selfsigned.key -out /etc/ssl/certs/selfsigned.crt
openssl dhparam -out /etc/nginx/dhparam.pem 4096


