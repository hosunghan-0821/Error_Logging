import certifi
import os
from flask import Flask, render_template, request, jsonify, Blueprint
from pymongo import MongoClient


app = Flask(__name__)
ca = certifi.where()

client = MongoClient('mongodb+srv://logging:12345@cluster0.wfh6y.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

delete_page = Blueprint('delete_page', __name__, template_folder='templates')


@delete_page.route('/log/delete', methods=["GET"])
def delete():
    write_num = request.args.get('write_num')
    result = db.write.find_one({'write_num': int(write_num)}, {'_id': False})
    # 기존 이미지 파일들
    prev_error_image = result['error_image']
    prev_solution_image = result['solution_image']


    # 서버에 저장된 이미지 삭제
    try:
        to_delete_file_path = prev_error_image.split("/")[-1]
        os.remove('./static/Images/' + to_delete_file_path)
    except:
        pass

    # 서버에 저장된 이미지 삭제
    try:
        to_delete_file_path = prev_solution_image.split("/")[-1]
        os.remove('./static/Images/' + to_delete_file_path)
    except:
        pass
    db.write.delete_one({'write_num': int(write_num)})
    return jsonify({'result': 'success'})
