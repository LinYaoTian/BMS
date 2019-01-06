import mysql.connector


def get_conn():
    return mysql.connector.connect(
        user='root',
        password='******',
        database='bms',
        use_unicode=True,)


ERROR_CODE = 1
OK_CODE = 0
SERVER_HEADER = 'http://10.1.1.241:8000'
