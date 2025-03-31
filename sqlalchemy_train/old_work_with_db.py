import pymysql


conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="rootpassword123",
    database="local_database",
)

cur = conn.cursor()


cur.execute(
    """
        SELECT * FROM Users;
    """
)

cur.execute(
    """
        CREATE TABLE table_name (
        id,
        field1,
        field2
        );
    """
)


cur.execute(
    """
        INSERT INTO table_name (id, field1, field2)
        VALUES (%s, %s, %s);
    """,
    ('val1', 'val2', 'val3')
)
