import cx_Oracle

def get_connection():
    dsn = cx_Oracle.makedsn("localhost", "1521", service_name="xe")
    connection = cx_Oracle.connect(user="c##hr2", password="1234", dsn=dsn)
    return connection