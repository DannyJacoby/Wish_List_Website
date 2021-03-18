import time

from flask import Flask, request, redirect, url_for, session, send_from_directory
from flask_cors import CORS
from flask_session import Session

from middleware import logged_in, is_admin


# As a note, all references to flask's app, hereby called api, is the app name in Procfile,
# while this file's name is the name bit of Procfile
# basically, if change "api", change Procfile's (web: gunicorn app:api) api's to new thing
api = Flask(__name__, static_folder="frontend/build", static_url_path="")
CORS(api)
Session(api)


# DB Configuration Stuff
# api.config['MYSQL_HOST'] = 'lyn7gfxo996yjjco.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
# api.config['MYSQL_USER'] = 'ur143du8y37j5on7'
# api.config['MYSQL_PASSWORD'] = 'phg6fzcay1hq1kon'
# api.config['MYSQL_DB'] = 'n5msszwbmtsqj22r'
# mysql = MySQL(api)


@api.route("/time")
def get_current_time():
    return {"time": time.time()}

@api.route("/")
@api.route("/index")
def index():
    return api.send_static_file("index.html")

@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return api.send_static_file("login.html")

    # POST
    else:
        return redirect(url_for("profile"))
    #   username = request.form.get("user")
    #   password = request.form.get("pass")
    # TODO: check if the user entered valid credentials
    #      - on success: set up their session and redirect to the landing page
    #      - on failure: render an error message


@api.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@api.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return api.send_static_file("create_account.html")

    # POST
    else:
        return redirect(url_for("profile"))
    #     username = request.form.get("user")
    #     password = request.form.get("pass")
    # TODO: check if the user entered valid credentials
    #      - on success: add them to the db and redirect to the landing page
    #      - on failure: render an error message


@api.route("/profile")
@logged_in
def profile():
    # TODO: add middleware so only logged in admin users can see this page
    return api.send_static_file("profile.html")


@api.route("/admin")
@logged_in
@is_admin
def admin():
    # TODO: add middleware function to make sure that a user must be logged
    #       in to see this page, and that they can only see their page
    return api.send_static_file("admin.html")
  
@api.errorhandler(404)
def not_found(e):
    return api.send_static_file("index.html")

if __name__ == '__main__':
    api.run()
    # api.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))
