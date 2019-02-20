#report_view
This project is most like a mini flask demo to store and show test report.
It contains the following files:

initdb.py: init a sqlite3 database
report_writer.py: convert a json result(from avocado) and add it to db
report_view.py: main app that display report

Quick start:
...
#pip install Flask
#pip install flask-bootstrap
#pip install flask_sqlalchemy
#pip install sqlalchemy
#./initdb.py # do not do it if you already do it
#./report_view.py
...
Then you can access it via: http://IP:8001

#Install jquery
# wget https://nodejs.org/dist/v6.11.4/node-v6.11.4-linux-x64.tar.xz
# tar xf node-v6.11.4-linux-x64.tar.xz
# export PATH=$PATH:$(pwd)
# npm install jquery
#/root/flask/npminstall/node-v6.11.4-linux-x64/bin/node_modules/jquery/src
