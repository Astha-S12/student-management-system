import os
import pymysql

def get_db_connection():
    return pymysql.connect(
        host=os.getenv("thomas.proxy.rlwy.net"),
        user=os.getenv("root"),
        password=os.getenv("DnLawNxZzqsGzPXWSWHLksNGkUtIkqFG"),
        database=os.getenv("railway"),
        port=int(os.getenv(58444)),
        cursorclass=pymysql.cursors.DictCursor
    )