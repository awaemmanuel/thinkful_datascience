import sqlite3 as lite
from pandas.io import sql

'''
    Constant property function.
'''
def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)


# Find the key with the greatest value
def keywithmaxval(d):
    return max(d, key = lambda k: d[k])


def _write_mysql(frame, table, names, cur):
    bracketed_names = ['`' + column + '`' for column in names]
    col_names = ','.join(bracketed_names)
    wildcards = ','.join([r'%s'] * len(names))
    insert_query = "INSERT INTO %s (%s) VALUES (%s)" % (
        table, col_names, wildcards)

    data = [[None if type(y) == float and np.isnan(y) else y for y in x] for x in frame.values]

    cur.executemany(insert_query, data)
    

def stringify_text(text):
    return '"' + str(text) + '"'


def connect_db(db_name):
    return lite.connect(db_name)