import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from database.db_manager import DBManager

def test_db_connection():
    db = DBManager()
    tablas = db.fetch_all("SELECT name FROM sqlite_master WHERE type='table';")
    print("Tablas en la base de datos:", tablas)
    db.close()

if __name__ == "__main__":
    test_db_connection()
