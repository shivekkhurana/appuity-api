Appuity
-----
App Store Reviews as a Service

### Requirements 
- Python 3.5+
- Postgres
- Unix based machine

### Setup 

1. Install virtualenv ([tutorial](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/))
2. Create a virtualenv named `appuity`
3. Activate `appuity`
4. git clone this repo
5. cd into source
6. pip install -r requirements.txt
7. cp config.sample.py config.py
8. Make changes to orator db connection in config.py
9. Run the migrations
10. invoke dev
