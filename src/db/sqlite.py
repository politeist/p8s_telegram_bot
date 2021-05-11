import os
import contextlib
import sqlite3

from typing import Optional

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

DB_PATH = f"{LOCAL_PATH}/../data/quiz.db"

print(DB_PATH)

class SQLite(object):
    def __init__(self, db: Optional[str] = DB_PATH):
        self.db=db
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db)
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        self.conn.commit()
        self.conn.close()

class DbConnection():
    def __init__(self, db: Optional[str] = None):
        if db:
            self.db = db
        else:
            self.db = DB_PATH

    def query(self, query: str) -> dict:
        _result = []
        with SQLite(self.db) as connector:
            values = connector.execute(query)
            colunms = list(map(lambda x: x[0], connector.description))
            values = connector.fetchall()
            for value in values:
                _result.append(dict(zip(colunms, value)))

        return _result
