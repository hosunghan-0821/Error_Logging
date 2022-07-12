from flask import Flask
import write

app = Flask(__name__)
app.register_blueprint(write.write_page)

if __name__=='__main__':
    app.run('0.0.0.0.', port=5000, debug=True)