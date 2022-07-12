from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient
import datetime
import hashlib
import jwt

main_page = Blueprint('main_page', __name__, template_folder='templates')

client = MongoClient('mongodb+srv://hosung:ghtjd114@Cluster0.rqdya.mongodb.net/?retryWrites=true&w=majority')
db = client.mini_project

SECRET_KEY = "error"

# 메인 페이지
@main_page.route('/')
def home():
    token_receive = request.cookies.get('user_token')
    print(token_receive)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload['user_nickname'])
        return render_template('index.html')
    except jwt.ExpiredSignatureError:
        print("쿠키만료")
        return render_template('index.html')
    except jwt.exceptions.DecodeError:
        print("decode 에러")
        return render_template('index.html')
