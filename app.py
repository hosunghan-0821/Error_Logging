from flask import Flask, render_template,request, jsonify
import login
import main
import signup


app = Flask(__name__)
app.register_blueprint(login.login_page)
app.register_blueprint(main.main_page)
app.register_blueprint(signup.signup_page)

if __name__=='__main__':
    app.run('0.0.0.0',port=5000,debug=True)