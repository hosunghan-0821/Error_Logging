import certifi
import jwt
import os
from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from datetime import datetime

import write

app = Flask(__name__)
ca = certifi.where()

client = MongoClient('mongodb+srv://logging:12345@cluster0.wfh6y.mongodb.net/Cluster0?retryWrites=true&w=majority',
                     tlsCAFile=ca)
db = client.dbsparta
SECRET_KEY = "error"

update_page = Blueprint('update_page', __name__, template_folder='templates')


@update_page.route('/log/update', methods=['GET'])
def update_page_():
    token_receive = request.cookies.get('user_token')
    write_num = request.args.get('write_num')
    print(write_num)
    result = db.write.find_one({'write_num': int(write_num)}, {'_id': False})
    print(result)
    if result is not None:
        try:
            payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            user_info = {'user_nickname': payload['user_nickname']}
            return render_template('update.html', user_info=user_info, result=result)
        except jwt.ExpiredSignatureError:
            user_info = {'user_nickname': False}
            return render_template('login.html', user_info=user_info)
        except jwt.exceptions.DecodeError:
            user_info = {'user_nickname': False}
            return render_template('login.html', user_info=user_info)
    else:
        print("해당 글 없음")
        return jsonify({"해당 글 없음": '글 없음'})


@update_page.route('/update', methods=['POST'])
def update():
    # 저장 날짜
    now = datetime.now()
    current_time = now.strftime("%Y년 %m월 %d일")

    # client로 부터 받은 데이터들
    title = request.form['title_give']
    detail_write = request.form['detail_give']
    solution_write = request.form['solution_give']
    user_nickname = request.form['user_nickname']
    write_num = request.form['write_num']

    result = db.write.find_one({'write_num': int(write_num)}, {'_id': False})

    # 기존 이미지 파일들
    prev_error_image = result['error_image']
    prev_solution_image = result['solution_image']

    # 업데이트 된 이미지 파일들
    error_image = request.files.get("error_image")
    solution_image = request.files.get("solution_image")

    # 업데이트 된 이미지가 존재하다면 기존 이미지 서버에서 삭제
    if error_image is not None:
        to_delete_file_path = prev_error_image.split("/")[-1]
        print(to_delete_file_path)
        os.remove('./static/Images/' + to_delete_file_path)

    if solution_image is not None:
        to_delete_file_path = prev_solution_image.split("/")[-1]
        print(to_delete_file_path)
        os.remove('./static/Images/' + to_delete_file_path)

    # write.py 에서 쓴 함수 import 해서 이미지 서버에 저장 재활용
    file_route = write.save_write_image_in_server(error_image, solution_image, write_num, True)

    # 사용자가 이미지를 안올릴 경우, 이전 이미지 경로를 계속  유지해야한다.
    if file_route['error_image_path'] == "":
        file_route['error_image_path'] = prev_error_image
    if file_route['solution_image_path'] == "":
        file_route['solution_image_path'] = prev_solution_image

    data = {
        'write_num': int(write_num),
        'user_nickname': user_nickname,
        'title': title,
        'detail': detail_write,
        'solution': solution_write,
        'error_image': file_route['error_image_path'],
        'solution_image': file_route['solution_image_path'],
        'date': current_time
    }
    db.write.replace_one({'write_num': int(write_num)}, data)

    return jsonify({"result": "success"})
