#!/bin/bash
echo Starting Redeemer Music app.
cd /var/www/flask
source redeemer_music/bin/activate
cd redeemer_music
gunicorn -w 2 -b 127.0.0.1:8080 app:app