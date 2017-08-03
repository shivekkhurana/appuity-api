from orator import Model, DatabaseManager
from config import databases

db = DatabaseManager(databases)
Model.set_connection_resolver(db)

def getDb():
	return db
	
class Base(Model):
    pass