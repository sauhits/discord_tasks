import psycopg2
from tabulate import tabulate as tab


host = "ep-lucky-lake-a19d5syz.ap-southeast-1.pg.koyeb.app"
dbname = "koyebdb"
user = "taskuser"
password = "qc2agkMpsG0d"
port = "5432"


def showTasks(cxt):
    try:
        cursor=dbConnect()
        sql = "SELECT * FROM mytask ORDER BY deadline DESC"
        cursor.execute(sql)
        tables = cursor.fetchall()
        dbClose(cursor)
        return tab(tables, headers=["ID", "タイトル", "期限"],tablefmt="simple")
    except Exception as e:
        print("エラー:", e)
        return None


def insertTask(cursor, title: str, deadline: str):
    sql = "INSERT INTO mytask(title,deadline) VALUES(%s,%s)"
    cursor.execute(sql, (title, deadline))


def deleteTask(cursor, id: int):
    sql = "DELETE FROM mytask WHERE id = %s"
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