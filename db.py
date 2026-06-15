import pymysql

def get_db_connection():
    try:
        conn = pymysql.connect(
            host="mysql.railway.internal",
            user="root",
            password="DnLawNxZzqsGzPXWSWHLksNGkUtIkqFG",
            database="railway",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✅ DB CONNECTED")
        return conn

    except Exception as e:
        print("❌ DB ERROR:", e)
        return None
    