import mariadb
from flask import request
import dbcreds
from uuid import uuid4

def connection():
    conn = None
    cursor = None
    try:
        conn = mariadb.connect(
                                user = dbcreds.user,
                                password = dbcreds.password,
                                host = dbcreds.host,
                                port = dbcreds.port,
                                database = dbcreds.database)
        print("connected")
        cursor = conn.cursor()
    except:
        if (cursor != None):
            cursor.close()
        print("cursor closed")
        if (conn != None):
            conn.close()
        print("connection closed")
        raise ConnectionError ("Could not establish a connection to the database")
    return (conn, cursor)


def login(userId):
    loginToken = uuid4().hex
    (conn, cursor) = connection()
    userId = cursor.execute('SELECT id FROM user WHERE username = ?', [request.json.get('username')])
    cursor.execute('INSERT INTO user_session (login_token, user_id) VALUES (?, ?)', [loginToken, userId])
    conn.commit()
    cursor.close()
    conn.close()
    return loginToken