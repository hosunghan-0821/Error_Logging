import certifi
import os

from flask import Flask, render_template, request, jsonify, Blueprint

app = Flask(__name__)

from pymongo import MongoClient

ca = certifi.where()

client = MongoClient('mongodb+srv://logging:12345@cluster0.wfh6y.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta

write_page = Blueprint('write_page', __name__, template_folder='templates')

@write_page.route('/log/write')
def home():
    return render_template('write.html')


@write_page.route("/write", methods=["POST"])
def error_logging_post():
    title = request.form['title_give']
    detail_write = request.form['detail_give']
    solution_write = request.form['solution_give']

    doc = {
        'title' : title,
        'detail' : detail_write,
        'solution' : solution_write,
    }

    db.write.insert_one(doc)

    return jsonify({'msg': '작성완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
