from app import app
from functions import connection
from flask import request, Response
import json
import mariadb

@app.route("/api/follows", methods=['GET', 'POST', 'DELETE'])
def userFollows():
    conn = None
    cursor = None
    (conn, cursor) = connection()
    if request.method == 'GET':
        params = request.args
        if params:
            userId = params.get('userId')
            cursor.execute("SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl from user INNER JOIN follow ON user.id = follow.followed WHERE follower =?",
                        [userId])
            result = cursor.fetchall()
            userArray = []
            for user in result:
                userDict = {
                    "userId" : user[0],
                    "email" : user[1],
                    "username" :user[2] ,
                    "bio" : user[3] ,
                    "birthdate" : user[4],
                    "imageUrl" : user[5],
                    "bannerUrl" : user[6]
                }
                userArray.append(userDict)
            return Response(json.dumps(userArray, default=str),
                        mimetype = 'application/json',
                        status = 200)    
        else:
            return Response("There was an error")
    
    elif request.method == 'POST':
        loginToken = request.json.get('loginToken')
        follow = request.json.get('followed')
        cursor.execute("SELECT user_id FROM user_session INNER JOIN follow ON follow.follower = user_session.user_id WHERE login_token = ?",
                        [loginToken,])
        result = cursor.fetchone()
        cursor.execute("SELECT id FROM user WHERE id = ?", [follow,] )
        followedUser = cursor.fetchall()
        followArray = []
        for user in followedUser:
            followDict = {
                "loginToken" : loginToken,
                "followId" : followedUser[0]
            }
            followArray.append(followDict)
        followId = None
        if cursor.rowcount == 1:
            follower = result[0]
            followId = followedUser[0][0]
            cursor.execute('INSERT INTO follow (follower, followed) WHERE follower = ?, followed = ?',[follower, followId])
            
            conn.commit()
            return Response("Success")
        else:
            return Response("error")
    elif request.method == 'DELETE':
        followId = request.json.get('userId')
        cursor.execute('SELECT followed from follow WHERE follower = ?', [followId,])
    