# Flask/DB Imports
from flask import Flask, request, redirect, url_for, session, send_from_directory
from flask_cors import CORS
from flask_session import Session

# Non Flask/DB imports
import time
from middleware import logged_in, is_admin

# As a note, all references to flask's app, hereby called api, is the app name in Procfile,
# while this file's name is the name bit of Procfile
# basically, if change "api", change Procfile's (web: gunicorn app:api) api's to new thing
api = Flask(__name__, static_folder="frontend/build", static_url_path="")
api.secret_key = "eTmic_1_EPw8UTpxt7xMJQ"
api.config["SESSION_TYPE"] = "filesystem"
CORS(api)
Session(api)


def _session_create(username, is_admin):
    session["user"] = username
    session["is_admin"] = is_admin


def _session_destroy():
    session.pop("user", None)
    session.pop("is_admin", None)

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
        username = request.form.get("user")
        password = request.form.get("pass")

        _session_create(username, False)

        return redirect(url_for("profile")) if username is not None else Response("Username/Password not found",
                                                                                  mimetype="text/plain", status=401)
    # TODO: check if the user entered valid credentials
    #      - on success: set up their session and redirect to the landing page
    #      - on failure: render an error message


@api.route('/logout')
def logout():
    _session_destroy()
    return redirect(url_for('index'))


@api.route("/create_account", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return api.send_static_file("create_account.html")

    # POST
    else:
        username = request.form.get("user")
        password = request.form.get("pass")

    _session_create(username, False)

    return redirect(url_for("profile")) if username is not None else Response("Failed to create account",
                                                                              mimetype="text/plain", status=500)
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
@admin
def admin():
    # TODO: add middleware function to make sure that a user must be logged
    #       in to see this page, and that they can only see their page
    return api.send_static_file("admin.html")


@api.errorhandler(404)
def not_found(e):
    return api.send_static_file("index.html")


if __name__ == '__main__':
    # put all "to be run"
    api.run()
    # api.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))

def setupApp():
    return 0
