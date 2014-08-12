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

    print("Database initialized!")



def db_update_location(location_key, location_dict):
    global db

    db_cursor = db.cursor()

    for connector in location_dict["connectors"]:
        try:
            # Get or create connector id
            connector_id = db_get_connector_id(db_cursor, location_key, connector["variant"])
            if connector_id is None:
                db_cursor.execute("INSERT INTO connector (location_key, connector_variant) VALUES (%s, %s)", (location_key, connector["variant"]))
                connector_id = db_get_connector_id(db_cursor, location_key, connector["variant"])

            # Update downtime
            print("%s" % connector_id)

        except BaseException as e:
            print("Error: %s" % e.message)

    db.commit()


def db_get_connector_id(db_cursor, location_key, connector_variant):
    try:
        db_cursor.execute("SELECT id FROM connector WHERE location_key=%s AND connector_variant=%s", (location_key, connector_variant))
        row = db_cursor.fetchone()
        return row[0]
    except BaseException:
        return None
