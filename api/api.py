from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
import time

api = Flask(__name__, static_folder='./build', static_url_path='/')

@app.route("/time")
@cross_origin()
def get_current_time():
    return {"time": time.time()}

@app.route('/')
@cross_origin()
def index():
    return "<h1>Welcome to our Server!!</h1>"

@app.route('/index')
@cross_origin()
def homepage():
    return send_from_directory(app.static_folder,'index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT',80))
