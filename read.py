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



read_page = Blueprint('read_page', __name__, template_folder='templates')
@read_page.route('/log/read')
def read():

    token_receive = request.cookies.get('user_token')
    write_num = request.args.get('write_num')
    result = db_write.write.find_one({'write_num': int(write_num)}, {'_id': False})
    print(result)

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload['user_nickname'])
        user_info = {'user_nickname': payload['user_nickname']}
        return render_template('read.html', user_info=user_info, details=result)
    except jwt.ExpiredSignatureError:
        user_info = {'user_nickname': False}
        return render_template('read.html', user_info=user_info, details=result )
    except jwt.exceptions.DecodeError:
        user_info = {'user_nickname': False}
        return render_template('read.html', user_info=user_info, details=result)

