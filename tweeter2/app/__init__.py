from flask import Flask

app = Flask(__name__)

from endpoints import users, user_session, follows, followers, tweets, tweetLikes, comments, commentLikes
