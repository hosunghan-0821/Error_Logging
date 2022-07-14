import hashlib

from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient
import os
import datetime
import jwt

SECRET_KEY = "error"

# DB접근 관련
client = MongoClient('mongodb+srv://hosung:ghtjd114@Cluster0.rqdya.mongodb.net/?retryWrites=true&w=majority')
db = client.mini_project

signup_page = Blueprint('signup_page', __name__, template_folder='templates')


@signup_page.route('/log/signup')
def login():
    return render_template('signup.html')


@signup_page.route('/log/signup/verify', methods=["POST"])
def verify():

    user_id = request.form['user_id']
    user_pw = request.form['user_pw']
    user_nick = request.form['user_nickname']
    user_pw_hash = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()
    doc = {'user_id': user_id, 'user_pw': user_pw_hash, 'user_nickname': user_nick}
    db.user.insert_one(doc)
    # JWT 토큰을 만들어서 client에 반환해준다
    payload = {
        'user_id': user_id,
        'user_nickname': user_nick,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return jsonify({'result': 'success', 'token': token})


@signup_page.route('/check/duplicate', methods=["POST"])
def duplicate_check():
    check_item = request.form['check_item']
    check_value = request.form['check_value']
    result = db.user.find_one({check_item: check_value})
    if result is not None:
        return jsonify({"result": "fail"})
    else:
        return jsonify({"result": "success"})
