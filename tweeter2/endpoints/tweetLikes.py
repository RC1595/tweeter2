from app import app
from functions import connection
from flask import request, Response
import json
import mariadb


@app.route("/api/tweetLikes", methods=['GET', 'POST', 'DELETE'])
def tweetLikes():
    pass