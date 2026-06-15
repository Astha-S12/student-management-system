import pymysql

def get_db_connection():
    return pymysql.connect(
        host="${{RAILWAY_PRIVATE_DOMAIN}}",
        user="root",
        password="${{MYSQL_ROOT_PASSWORD}}",
        database="${{MYSQL_DATABASE}}",
        port=3306,
        cursorclass=pymysql.cursors.DictCursor
    )