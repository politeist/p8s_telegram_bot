import os

from db.sqlite import SQLite, DbConnection

LOCAL_PATH = os.path.dirname(os.path.abspath(__file__))

DB_PATH = f"{LOCAL_PATH}/quiz_test.db"


def test_sqlite():
	with SQLite(DB_PATH) as my_conn:
		assert os.path.isfile(DB_PATH)
		my_conn.execute("SELECT 1")
		res = list(my_conn.fetchall()[0])
		assert res == [1]


def test_db_connection_query():
	db_conn = DbConnection(DB_PATH)
	assert db_conn.db == DB_PATH
	res = db_conn.query("SELECT 1")
	assert res == [{'1': 1}]
