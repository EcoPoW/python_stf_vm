
import os

import rocksdb

conn = None
def get_conn():
    global conn
    if conn:
        return conn

    conn = rocksdb.DB('test.db', rocksdb.Options(create_if_missing=True))
    return conn

