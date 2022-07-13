from flask import Blueprint, render_template, request, jsonify
from pymongo import MongoClient
import certifi

ca = certifi.where()

client = MongoClient('mongodb+srv://logging:12345@cluster0.wfh6y.mongodb.net/Cluster0?retryWrites=true&w=majority',tlsCAFile=ca)
db = client.dbsparta


read_page = Blueprint('read_page', __name__, template_folder='templates')
@read_page.route('/log/read')
def read():
    return render_template('read.html')

