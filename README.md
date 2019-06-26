# report_view
This project is most like a mini flask demo to store and show test report.
It contains the following files:

* initdb.py: init a sqlite3 database
* report_writer.py: convert a json result(from avocado) and add it to db
* report_view.py: main app that display report

Quick start:
```
#pip install Flask
#pip install flask-bootstrap
#pip install flask_sqlalchemy
#pip install sqlalchemy
#./initdb.py # do not do it if you already do it
#python manager.py runserver -h 0.0.0.0 -p 8001
```
Then you can access it via: http://IP:8001

