from app import app
from functions import connection
from werkzeug.datastructures import iter_multi_items
from flask import request, Response
import json


conn = None
cursor = None

@app.route("/api/users", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users():
    (conn, cursor) = connection()
    if request.method == 'GET':
        params = request.args
        user = "user"
        print(params)
        if not params:
            cursor.execute("SELECT username, bio, id, email FROM user")            
            # if (cursor.rowcount != 1):
            user = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]                
            print(user)
        elif params:
            userId = params.get('userId') 
            cursor.execute("SELECT username, bio, id, email FROM user WHERE id=?", [userId,])
            user = [dict((cursor.description[i][0], value) for i, value in enumerate(key)) for key in cursor.fetchall()] 
            print(user)
        return Response(json.dumps(user),
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
        
        if new_user != None:
            if (cursor.rowcount == 1):
                conn.commit()
                print(new_user)
                
            return Response(json.dumps(new_user),
                            mimetype = 'application/json',
                            status=201)
        else:
            return Response("Error",
                                mimetype = 'text/plain',
                                status = 400) 
            
        # elif request.method == 'PATCH':
        #     new_user = "NewUser"
        #     if new_user != None:
        #         user[1] = new_user
        #         print(user)
        #         return Response("Successful PATCH",
        #                         mimetype= 'text/plain',
        #                         status = 200)
        #     else:
        #         return Response("PATCH error",
        #                         mimetype = 'text/plain',
        #                         status = 400
        #                         )
        # elif request.method == 'DELETE':
        #     user.remove('user3')
        #     print(user)
        #     return Response("user removed",
        #                     mimetype = 'text/plain',
        #                     status = 200)



