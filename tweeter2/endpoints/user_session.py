from app import app
from flask import request, Response
import json
from uuid import uuid4
from functions import connection






@app.route("/api/login", methods=['POST', 'DELETE'])
def checkCreds():
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

def login(userId):
    loginToken = uuid4().hex
    (conn, cursor) = connection()
    cursor.execute('INSERT INTO user_session (login_token, user_id) VALUES (?, ?)', [loginToken, userId])
    conn.commit()
    cursor.close()
    conn.close()
    return loginToken
    
        
        
# while True:
#     print(uuid4().hex)
    
    
    
    

