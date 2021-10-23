from app import app
from functions import connection
from flask import request, Response
import json
import mariadb


@app.route("/api/comments", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def comments():
    pass