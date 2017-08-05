from orator import Model, DatabaseManager
from config import databases

db = DatabaseManager(databases)
Model.set_connection_resolver(db)
    
class Base(Model):
    def bulk_insert(self, records):
        return db.table(self.get_table()).insert(records)

    def find_or_create(self, record):
        found = db.table(self.get_table()).where(record).first()
        if not found:
            new_id = db.table(self.get_table()).insert_get_id(record)
            found = db.table(self.get_table()).where({'id': new_id}).first()

        return found
        


        



