import sqlite3


def setup_db(db_name, table_name):
    connection = sqlite3.connect(
        db_name
    )
    cursor = connection.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS """
        + table_name
        + """  
                      (id INTEGER PRIMARY KEY, name TEXT)"""
    )
    connection.commit()
    connection.close()
