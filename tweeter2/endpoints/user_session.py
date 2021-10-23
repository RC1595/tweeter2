from app import app
from flask import request, Response
import json
from uuid import uuid4
from functions import connection
import mariadb



@app.route("/api/login", methods=['POST', 'DELETE'])
def checkCreds():
    try:
        conn = None
        cursor = None
        (conn, cursor) = connection()
        
        if request.method == 'POST':
            email = request.json.get('email')
            pwrd = request.json.get('password')
            cursor.execute('SELECT * FROM user WHERE email = ? AND password = ?',[email,pwrd])
            result = cursor.fetchall()
            if (cursor.rowcount == 1):
                if pwrd == result[0][3]:
                    userId = result[0][0]
                    loginToken = login(userId)
                    dict = {
                        "userId" : userId,
                        "loginToken" : loginToken
                    }
                    return Response (json.dumps(dict),
                            mimetype='application/json',
                            status= 200)
            else:
                return Response("Credentials do not match.",
                                mimetype= 'text/plain',
                                status=401)
        elif request.method == 'DELETE':
            token = request.json.get('loginToken')
            cursor.execute('SELECT * from user_session WHERE login_token =?', [token,])
            result = cursor.fetchall()
            if (cursor.rowcount == 1):
                cursor.execute('DELETE FROM user_session WHERE login_token = ?', [token,])
                conn.commit()
                cursor.close()
                conn.close()
                return Response(mimetype='application/json',
                                status=204)
            else:
                return Response ("there was an error")
            
            
            
    except ConnectionError:
        return Response ("There was a problem connecting to the database",
                        mimetype= 'text/plain',
                        status= 400)
    except mariadb.DataError:
        return Response ("There was a problem processing your request",
                        mimetype= 'text/plain',
                        status= 400)
    except mariadb.OperationalError:
        return Response ("Operational error on connection",
                        mimetype='text/plain',
                        status= 400)
    except mariadb.ProgrammingError:
        return Response ("Bad query",
                        mimetype='text/plain',
                        status= 400)
    except mariadb.IntegrityError:
        return Response ("Harmful query detected",
                        mimetype= 'text/plain',
                        status= 403)
    finally:
        if (cursor != None):
            cursor.close()
        if (conn != None):
            conn.close()
            

def login(userId):
    loginToken = uuid4().hex
    (conn, cursor) = connection()
    cursor.execute('INSERT INTO user_session (login_token, user_id) VALUES (?, ?)', [loginToken, userId])
    conn.commit()
    cursor.close()
    conn.close()
    return loginToken
