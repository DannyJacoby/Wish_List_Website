from flask import Flask, send_from_directory
from flask_cors import CORS, cross_origin
import time

# As a note, all references to flask's app, hereby called api, is the app name in Procfile, 
# while this file's name is the name bit of Procfile
# basically, if change "api", change Procfile's (web: gunicorn app:api) api's to new thing
api = Flask(__name__, static_folder='frontend/build', static_url_path='')


# DB Configuration Stuff
api.config['MYSQL_HOST'] = 'lyn7gfxo996yjjco.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
api.config['MYSQL_USER'] = 'ur143du8y37j5on7'
api.config['MYSQL_PASSWORD'] = 'phg6fzcay1hq1kon'
api.config['MYSQL_DB'] = 'n5msszwbmtsqj22r'
mysql = MySQL(api)


@api.route("/time")
@cross_origin()
def get_current_time():
    return {"time": time.time()}

@api.route('/', methods=['GET','POST'])
@cross_origin()
def index():
    firstname = "shwan"
    lastname = "johnson"
    success = False
    if request.method == "POST":
        cur = mysql.connenction.cursor()
        cur.execute("INSERT INTO myusers(firstname, lastname) VALUES (%s, %s)", (firstname, lastname))
        mysql.connection.commit()
        cur.close()
        success = True
        return 'success'
    Str = "have " if success else "have not"
    return "<h1>Welcome to our Server " + firtname + " " + lastname + "!! You " + Str + " been added!</h1>"

@api.route('/index')
@cross_origin()
def homepage():
    return send_from_directory(api.static_folder,'index.html')

@api.errorhandler(404)
def not_found(e):
    return api.send_static_file('index.html')

if __name__ == '__main__':
    api.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT',80))
