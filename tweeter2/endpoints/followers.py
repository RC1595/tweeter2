
from app import app
from functions import connection
from flask import request, Response
import json
import mariadb

@app.route("/api/followers", methods=['GET'])
def followers():
    conn = None
    cursor = None
    (conn, cursor) = connection()
    if request.method == 'GET':
        params = request.args
        if params:
            userId = params.get('userId')
            cursor.execute('SELECT follower FROM follow WHERE followed = ?', [userId,])
            # ("SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl from user INNER JOIN follow ON user.id = follow.followed WHERE followed =?",
            #             [userId,])
            
            
            followers = cursor.fetchall()
            print(followers)
            for follower in followers:
                cursor.execute('SELECT id, email, username, bio, birthdate, imageUrl, bannerUrl FROM user WHERE id =?', [follower[0],])
                
                result = cursor.fetchall()
                
            return Response(json.dumps(result, default=str),
                            mimetype='application/json',
                            status= 200)
        else:
            return Response("error")
