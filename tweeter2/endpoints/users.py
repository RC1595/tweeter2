from app import app
from functions import connection
from functions import login
from werkzeug.datastructures import iter_multi_items
from flask import request, Response
import json


@app.route("/api/users", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users():
    conn = None
    cursor = None
    (conn, cursor) = connection()
    if request.method == 'GET':
        params = request.args
        user = "user"
        print(params)
        if not params:
            cursor.execute("SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user")            
            user = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]                
            print(user)
        elif params:
            userId = params.get('userId') 
            cursor.execute("SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE id=?", [userId,])
            user = [dict((cursor.description[i][0], value) for i, value in enumerate(key)) for key in cursor.fetchall()] 
            print(user)
        return Response(json.dumps(user, default=str),
                        mimetype = 'application/json',
                        status = 200)
            
    elif request.method == 'POST':
        new_user = request.json.get('username')
        cursor.execute("INSERT INTO user (email, username, password, birthdate, bio, imageUrl, bannerUrl) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    [request.json.get('email'),
                    request.json.get('username'),
                    request.json.get('password'),
                    request.json.get('birthdate'),
                    request.json.get('bio'),
                    request.json.get('imageUrl'),
                    request.json.get('bannerUrl')])
        userId = cursor.execute('SELECT id FROM user WHERE username = ?', [new_user,])
        loginToken = login(userId)
        if new_user != None:
            cursor.execute('SELECT userId, email, username, bio, imageUrl, bannerUrl from user INNER JOIN user_session ON user.id = user_session.user_id WHERE login_token =?', [loginToken])
            result = cursor.fetchall()
            userArray = []
            for user in result:
                userDict = {
                "userId" : user[0],
                "email" : user[1],
                "username" : user[2],
                "bio" : [3],
                "imageUrl" : [4],
                "bannerUrl" : [5],
                "loginToken" : loginToken
                }
                userArray.append(userDict)
                conn.commit()
                print(userDict)
                
            return Response(json.dumps(userDict),
                            mimetype = 'application/json',
                            status=201)
        else:
            return Response("Error",
                                mimetype = 'text/plain',
                                status = 400) 
            
    elif request.method == 'PATCH':
        cursor.execute("SELECT user_id FROM user_session WHERE login_token = ?",
                    [request.json.get('loginToken'),])
        result = cursor.fetchall()
        userId = result[0][0]
    
        if userId != None:
            cursor.execute("SELECT * FROM user WHERE id = ?", [userId])
            currentUser = cursor.fetchall()
            if cursor.rowcount == 1:
                if request.json.get('email') != None:
                    cursor.execute("UPDATE user SET email=? WHERE id=?",[request.json.get('email'), userId])
                else:
                    pass
                if request.json.get('username') != None:
                    cursor.execute("UPDATE user SET username=? WHERE id=?",[request.json.get('username'), userId])
                else:
                    pass
                if request.json.get('password') != None:
                    cursor.execute("UPDATE user SET password=? WHERE id=?",[request.json.get('password'), userId])
                else:
                    pass
                if request.json.get('birthdate') != None:
                    cursor.execute("UPDATE user SET birthdate=? WHERE id=?",[request.json.get('birthdate'), userId])
                else:
                    pass
                if request.json.get('bio') != None:
                    cursor.execute("UPDATE user SET bio=? WHERE id=?",[request.json.get('bio'), userId])
                else:
                    pass
                cursor.execute("UPDATE user SET imageUrl=? WHERE id=?",[request.json.get('imageUrl'), userId])
                cursor.execute("UPDATE user SET bannerUrl=? WHERE id=?",[request.json.get('bannerUrl'), userId])
                conn.commit()
                cursor.execute("SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl from user WHERE id = ?", [userId])
                currentUser = cursor.fetchall()
                userArray = []
                for user in currentUser:
                    userDict = {
                        "userId" : currentUser[0][0],
                        "email" : currentUser[0][1],
                        "username" : currentUser[0][2],
                        "bio" : currentUser[0][3],
                        "birthdate" : currentUser[0][4],
                        "imageUrl" : currentUser[0][5],
                        "bannerUrl" : currentUser[0][6]
                    }
                userArray.append(userDict)
                return Response(json.dumps(userDict, default=str),
                                mimetype= 'application/json',
                                status = 200)
            else:
                return Response("There was an error accessing your information. Please make sure you are logged in and try again")
        else:
            return Response("PATCH error",
                                mimetype = 'text/plain',
                                status = 400
                                )
    elif request.method == 'DELETE':
        cursor.execute("SELECT user_id FROM user_session WHERE login_token = ?", [request.json.get('loginToken'),])
        result = cursor.fetchall()
        thisUser = None
        if cursor.rowcount == 1:
            thisUser = result[0][0]
            cursor.execute("DELETE FROM user WHERE id=?", [thisUser])
            conn.commit()
        else:
            return Response("There was an error processing your request")
        
        
    return Response("user removed",
                            mimetype = 'text/plain',
                            status = 200)



