
import os

import rocksdb
import mpt

conn = None
def get_conn():
    global conn
    if conn:
        return conn

    conn = rocksdb.DB('test.db', rocksdb.Options(create_if_missing=True))
    return conn

get_conn()


class DBWrap:
    def __init__(self, db) -> None:
        self.db = db

    def __setitem__(self, key, value):
        self.db.put(key, value)

    def __getitem__(self, key):
        return self.db.get(key)


# conn = rocksdb.DB('test.db', rocksdb.Options(create_if_missing=True))
def get_mpt(root=None):
    # storage = {}
    storage = DBWrap(conn)
    m = mpt.MerklePatriciaTrie(storage, root=root)
    return m
