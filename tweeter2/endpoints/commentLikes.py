from app import app
from functions import connection
from flask import request, Response
import json
import mariadb



@app.route("/api/commentLikes", methods=['GET', 'POST', 'DELETE'])
def commentLikes():
    pass