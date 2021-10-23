from app import app
from functions import connection
from flask import request, Response
import json
import mariadb


@app.route("/api/tweets", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def tweets():
    conn = None
    cursor = None
    (conn, cursor) = connection()
    if request.method == 'GET':
        params = request.args
        userId = params.get('userId')
        if params:
            cursor.execute('SELECT * from tweet INNER JOIN user ON tweet.user_id = user.id WHERE user_id = ?', [userId,])
            userTweets = cursor.fetchall()
            tweetArray = []
            for tweet in userTweets:
                tweetDict = {
                    "tweetId" : tweet[0],
                    "userId" : tweet[1],
                    "username" : tweet[4],
                    "content" : tweet[2],
                    "CreatedAt" : tweet[3],
                    "userImageUrl" : tweet[10],
                    "tweetImageUrl" : tweet[11]
                }
                tweetArray.append(tweetDict)
            return Response(json.dumps(tweetArray, default=str),
                                mimetype= 'application/json',
                                status=200)
        else:
            return Response("This user does not have any tweets yet",
                            mimetype='text/plain',
                            status=400)
            
    
    elif request.method == 'POST':
        cursor.execute("SELECT user_id FROM user_session WHERE login_token = ?", [request.json.get('loginToken'),])
        result = cursor.fetchall()
        userId = None
        if cursor.rowcount == 1:
            userId = result[0][0]
            newTweet = request.json.get('content')
            cursor.execute('INSERT INTO tweet(user_id, content) VALUES (?,?)',  [userId, newTweet])
            conn.commit()
            cursor.execute('SELECT * FROM tweet INNER JOIN user ON tweet.user_id = user.id')
            tweets = cursor.fetchall()
            
            tweetArray = []
            for tweet in tweets:
                tweetDict = {
                    "tweetId" : tweet[0],
                    "userId" : tweet[1],
                    "username" : tweet[6],
                    "userImageUrl" : tweet[10],
                    "content" : tweet[2],
                    "createdAt" : tweet[3],
                    "imageUrl" : tweet[11]
                }
                tweetArray.append(tweetDict)
                print(tweetArray)
            return Response(json.dumps(tweetArray, default=str),
                            mimetype= 'application/json',
                            status=201)
        else:
            return Response("User does not exist",
                            mimetype='text/plain',
                            status=400)
            
            
    elif request.method == 'PATCH':
        cursor.execute("SELECT user_id FROM user_session WHERE login_token = ?", [request.json.get('loginToken'),])
        result = cursor.fetchall()
        userId = None
        if cursor.rowcount == 1:
            userId = result[0][0]
            cursor.execute('SELECT id, content FROM tweet WHERE user_id = ?', [userId])
            tweetId = cursor.fetchall()

            cursor.execute('UPDATE tweet SET content = ? WHERE id = ?', [request.json.get('content'), request.json.get('tweetId')])
            cursor.execute('SELECT id, content FROM tweet WHERE user_id = ?', [userId])
            updatedTweet = cursor.fetchall()
            idArray = []
            for tweet in updatedTweet:
                idDict = {
                    "tweetId" : tweet[0],
                    "content" : tweet[1]
                }
                idArray.append(idDict)
            print(updatedTweet)
            conn.commit()
            return Response(json.dumps(idArray, default=str),
                        mimetype='application.json',
                        status=200)
        else:
            return Response("Error",
                                    mimetype = 'text/plain',
                                    status = 400)
    elif request.method == 'DELETE':
        userId = request.json.get('userId')
        cursor.execute('SELECT login_token from user_session')
        token = cursor.fetchall()
        print(token)
        cursor.execute('SELECT tweet.id FROM tweet INNER JOIN user_session ON tweet.user_id = user_session.user_id')
        tweetId = cursor.fetchone()
        print(tweetId)

        if cursor.rowcount == 1:            
            cursor.execute('DELETE * from tweet WHERE id = ? AND login_Token = ?', [tweetId, token])
            conn.commit()
        else:
            return Response("You are trying to delete multiple tweets at once")
        return Response("Delete successful")    
