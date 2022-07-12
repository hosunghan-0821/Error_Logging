from flask import Blueprint, render_template, request, jsonify

read_page = Blueprint('read_page', __name__, template_folder='templates')
@read_page.route('/log/read')
def read():
    return render_template('read.html')