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
def home():
    write_num = request.args.get('write_num')
    db.write.delte_one({'write_num': write_num})
    return jsonify({'message': 'success'})
