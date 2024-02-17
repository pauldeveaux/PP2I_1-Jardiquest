from flask import g
import sqlite3

from jardiquest.setup_sql import database_path


# close the connection to the database call when the flask server is teardown
def close_connection(exception) -> None:
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# get the connection to the database
def get_db() -> (any or None):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database_path)
    return db

