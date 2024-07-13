#!/usr/bin/env bash
#A Bash script that sets up the web servers for the deployment
sudo apt-get -y update
sudo apt-get -y upgrade
sudo apt-get -y install nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

fake_HTML="<!DOCTYPE html>
<html lang=\"en\">
<head></head>
<body>
    <h1>Holberton School</h1>
</body>
</html>"

echo "$fake_HTML" | sudo tee /data/web_static/releases/test/index.html

sudo rm -rf /data/web_static/current
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default
sudo service nginx restart
