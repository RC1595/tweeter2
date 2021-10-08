import mariadb
from flask import Flask, request, Response
import json

app=Flask(__name__)

@app.route("/api/users", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def users():
    user = ['username', 'user2', 'user3']
    if request.method == 'GET':
        return Response(json.dumps(user),
                        mimetype = 'application/json',
                        status = 200)
    elif request.method == 'POST':
        new_user = 'newuser'
        if new_user != None:
            user.append(new_user)
            print(user)
            return Response("Welcome to Tweeter Two",
                            mimetype = 'text/plain',
                            status=201)
        else:
            return Response("Error",
                            mimetype = 'text/plain',
                            status = 400)
    elif request.method == 'PATCH':
        new_user = "NewUser"
        if new_user != None:
            user[1] = new_user
            print(user)
            return Response("Successful PATCH",
                            mimetype= 'text/plain',
                            status = 200)
        else:
            return Response("PATCH error",
                            mimetype = 'text/plain',
                            status = 400
                            )
    elif request.method == 'DELETE':
        user.remove('user3')
        print(user)
        return Response("user removed",
                        mimetype = 'text/plain',
                        status = 200)



app.run(debug=True)