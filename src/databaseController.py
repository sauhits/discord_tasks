import psycopg2

host = "localhost"
dbname = "mytask"
user = "taskuser"
password = "kadai"
port = "5433"


def showTasks(cursor):
    sql = "SELECT * FROM task ORDER BY limit_date DESC"
    cursor.execute(sql)
    tables = cursor.fetchall()
    return tables


def insertTask(cursor, name: str, limit_date: str):
    sql = "INSERT INTO task(name,limit_date) VALUES(%s,%s)"
    cursor.execute(sql, (name, limit_date))


def deleteTask(cursor, id: int):
    sql = "DELETE FROM task WHERE id = %s"
    cursor.execute(sql, id)


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
