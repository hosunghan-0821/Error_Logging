import certifi
import os
from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
ca = certifi.where()

client = MongoClient('mongodb+srv://logging:12345@cluster0.wfh6y.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

write_page = Blueprint('write_page', __name__, template_folder='templates')

@write_page.route('/log/write')
def home():
    return render_template('write.html')


@write_page.route("/write", methods=["POST"])
def error_logging_post():
    doc = db.counters.find_one({'$and': [{"collections": 'error_record'}, {"seq": {"$exists": True}}]})
    if doc is None:
        db.counters.update_one({"collections": "error_record"}, {"$set": {'seq': 1}})
        seq = 1
    else:
        db.counters.update_one({"collections": "error_record"}, {"$set": {'seq': doc['seq'] + 1}})
        seq = doc['seq'] + 1

    # 오류 게시글 고유 번호
    write_num = seq

    # 제목 , 오류 상세설명 text, # 해결방안 상세설명
    title = request.form['title_give']
    detail_write = request.form['detail_give']
    solution_write = request.form['solution_give']

    error_image = request.files.get("error_image")
    solution_image = request.files.get("solution_image")
    # 이미지 넘겨 받고 서버 컴에 저장하는 함수
    file_route = save_write_image_in_server(error_image,solution_image, write_num)

    # 서버에 이미지 접속하기 위한 url
    print(file_route)

    # 저장 날짜
    now = datetime.now()
    current_time = now.strftime("%Y년 %m월 %d일")

    # 저장 데이터
    data = {
        'write_num': write_num,
        'title': title,
        'detail': detail_write,
        'solution': solution_write,
        'error_image': file_route['error_image_path'],
        'solution_image': file_route['solution_image_path'],
        'date': current_time
    }

    # db에 저장하기
    db.write.insert_one(data)
    return jsonify({'msg': '작성완료!'})


def save_write_image_in_server(error_image, solution_image, write_num):

    # 현재시간 가져와서 이미지 파일명으로 사용
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")

    # 서버에 저장된 이미지에 접근할 수 있는 경로 작성 (ip/port/directory 활용)
    file_route = {}
    server_ip_port = "127.0.0.1:5000"
    route = "/static/Images/"

    # 파일명 규칙에 맞게 작성.
    # 이미지 1개씩 저장 했기 때문에 for문 없이 하드 코딩식으로 작성했음
    error_file = str(write_num) + "_" + current_time + "_error" + ".jpg"
    solution_file = str(write_num) + "_" + current_time + "_solution" + ".jpg"

    # 서버컴에 이미지 저장
    error_image.save(os.path.join("./static/Images/", secure_filename(error_file)))
    solution_image.save(os.path.join("./static/Images/", secure_filename(solution_file)))

    # error , solution 이미지 경로 저장
    error_file_path = "http://"+server_ip_port + route + error_file
    solution_file_path = "http://"+server_ip_port + route + solution_file

    # 파일 경로 dictionary 형태로 저장
    file_route['error_image_path'] = error_file_path
    file_route['solution_image_path'] = solution_file_path

    return file_route


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
