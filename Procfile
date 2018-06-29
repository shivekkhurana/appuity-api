web: gunicorn app:app
init: cp config.sample.py config.py
migrate: orator migrate -c config.py
seed-apps: invoke populate_apps_table