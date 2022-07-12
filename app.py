from flask import Flask, render_template
import read

app = Flask(__name__)

app.register_blueprint(read.read_page)

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
