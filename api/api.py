import time
from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='frontend/build', static_url_path='')


@app.route("/time")
@cross_origin()
def get_current_time():
    return {"time": time.time()}

@app.route('/')
@cross_origin()
def index():
    return "Welcome to our Server!!"

@app.route('/index')
@cross_origin()
def homepage():
    return send_from_directory(app.static_folder,'index.html')
    

if __name__ == '__main__':
    app.run()
