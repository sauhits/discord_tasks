import psycopg2

host = "localhost"
dbname = "mytask"
user = "taskuser"
password = "kadai"
port = "5433"


def dbConnect():
    try:
        connection = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        print("Connected to database")
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        print("接続エラー:", e)
        return None


def dbClose(cursor):
    if cursor:
        cursor.close()
        print("データベース接続を閉じました。")
    else:
        print("接続がありません。")
