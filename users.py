import mariadb
import dbcreds
from flask import Flask, request, Response
import json
from dict import userInfo

app=Flask(__name__)

try:
    conn = mariadb.connect(
        user = dbcreds.user,
        password = dbcreds.password,
        host = dbcreds.host,
        port = dbcreds.port,
        database = dbcreds.database)
    print("connected")
    cursor = conn.cursor()

    @app.route("/api/users", methods=['GET', 'POST', 'PATCH', 'DELETE'])
    def users():
        
        if request.method == 'GET':
            cursor.execute("SELECT username, bio, id, email FROM user")
            user = cursor.fetchall()
            print(user)
            return Response(json.dumps(user),
                            mimetype = 'application/json',
                            status = 200)
            
        # elif request.method == 'POST':
        #     new_user = 'newuser'
        #     if new_user != None:
        #         user.append(new_user)
        #         print(user)
        #         return Response("Welcome " +new_user+ " to Tweeter Two",
        #                         mimetype = 'text/plain',
        #                         status=201)
        #     else:
        #         return Response("Error",
        #                         mimetype = 'text/plain',
        #                         status = 400)
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
except:
    print("no connection")

# finally:
#     if (cursor != None):
#         cursor.close()
#     print("cursor closed")
#     if (conn != None):
#         conn.close()
#     print("connection closed")


app.run(debug=True)