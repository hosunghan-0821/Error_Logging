from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient
import datetime
import hashlib
import jwt
import certifi

main_page = Blueprint('main_page', __name__, template_folder='templates')
client = MongoClient('mongodb+srv://hosung:ghtjd114@Cluster0.rqdya.mongodb.net/?retryWrites=true&w=majority')
db = client.mini_project

ca = certifi.where()
write = MongoClient('mongodb+srv://logging:12345@cluster0.wfh6y.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db_write = write.dbsparta


SECRET_KEY = "error"

# 메인 페이지
@main_page.route('/')
def home():
    token_receive = request.cookies.get('user_token')
    # print(token_receive)
    all_records = list(db_write.write.find({}, {"_id": False}).sort("write_num", -1))
    print(all_records)
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload['user_nickname'])
        user_info = {'user_nickname': payload['user_nickname']}
        return render_template('index.html', user_info=user_info, records=all_records)
    except jwt.ExpiredSignatureError:
        user_info = {'user_nickname': False}
        return render_template('index.html', user_info=user_info, records=all_records)
    except jwt.exceptions.DecodeError:
        user_info = {'user_nickname': False}
        return render_template('index.html', user_info=user_info, records=all_records)
