from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient
import datetime
import hashlib
import jwt

login_page = Blueprint('login_page', __name__, template_folder='templates')

client = MongoClient('mongodb+srv://hosung:ghtjd114@Cluster0.rqdya.mongodb.net/?retryWrites=true&w=majority')
db = client.mini_project

SECRET_KEY = "error"


# 로그인 화면 rendering
@login_page.route('/log/login')
def login():
    return render_template('login.html')


# 로그인 확인 후 ,jwt 토큰 발급
@login_page.route('/log/login/verify', methods=["POST"])
def verify():
    user_id = request.form['user_id']
    user_pw = request.form['user_pw']
    user_pw_hash = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()

    doc = {'user_id': user_id, 'user_pw': user_pw_hash}
    # client로 부터 받은 user 정보로 db 긁어서, 데이터 존재하는지 확인
    result = db.user.find_one(doc)


    # 유저정보가 존재한다면
    if result is not None:
        # JWT 토큰을 만들어서 client에 반환해준다
        payload = {
            'user_id': user_id,
            'user_nickname': result['user_nickname'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=300)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'msg': 'fail'})
