try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

import MySQLdb

from database_settings import db_host, db_user, db_passwd, db_name


def setup_database():
    print("Initializing database...")

    global db
    db = MySQLdb.connect(host=db_host(),
                         user=db_user(),
                         passwd=db_passwd(),
                         db=db_name())

    global db_cursor
    db_cursor = db.cursor()

    print("Database initialized!")

def database_cursor():
    global db_cursor
    return db_cursor
