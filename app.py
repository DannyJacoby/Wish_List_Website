from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
import time

api = Flask(__name__, static_folder='frontend/build', static_url_path='')

@api.route("/time")
@cross_origin()
def get_current_time():
    return {"time": time.time()}

@api.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to our Server!!</h1>"

@api.route('/index')
@cross_origin()
def homepage():
    return send_from_directory(api.static_folder,'index.html')

@api.errorhandler(404)
def not_found(e):
    return api.send_static_file('index.html')

if __name__ == '__main__':
    api.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT',80))