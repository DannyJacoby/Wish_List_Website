# Flask/DB Imports
from flask import Flask, Response, request, redirect, url_for, session, render_template
from flask_cors import CORS
from flask_session import Session
from sqlalchemy import create_engine, Table, MetaData
import cymysql

# Non Flask/DB imports
import time
from middleware import logged_in, is_admin

# As a note, all references to flask's app, hereby called api, is the app name in Procfile,
# while this file's name is the name bit of Procfile
# basically, if change "api", change Procfile's (web: gunicorn app:api) api's to new thing
api = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
api.secret_key = "eTmic_1_EPw8UTpxt7xMJQ"
api.config["SESSION_TYPE"] = "filesystem"
CORS(api)
Session(api)

herokuConnection = 'mysql+cymysql://ur143du8y37j5on7:phg6fzcay1hq1kon@lyn7gfxo996yjjco.cbetxkdyhwsb.us-east-1.rds.amazonaws.com/n5msszwbmtsqj22r'
localHostConnection = 'mysql+cymysql://root:password@localhost/master'

engine = create_engine(herokuConnection, convert_unicode=True)

metadata = MetaData(bind=engine)

# use this to call and find any users/lists/items, have to test about too many pings to DB issue (normally present in 336 final)
users = Table('user', metadata, autoload=True)
lists = Table('list', metadata, autoload=True)
items = Table('item', metadata, autoload=True)

con = engine.connect()

# list of columns in DB
# users - userid [INT]; username [string 45]; userpassword [string 45]; isadmin [1 is true, 0 is false]
# lists - primarylistid [INT]; listid [INT]; userid [INT]; itemid [INT]; itemposition [INT]; priority [1 is true, 0 is false]
# items - itemid [INT]; url [string 500]; description [string 500]; imageurl [string 500]; title [string 100]
# all DB query calls can be referenced here https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/

def _session_create(username, is_admin):
    session["user"] = username
    session["is_admin"] = is_admin


def _session_destroy():
    session.pop("user", None)
    session.pop("is_admin", None)

@api.route("/time")
def get_current_time():
    user1name = users.select(users.c.userid == 1).execute().first()

    return {
        "time": time.time(),
        "user1": user1name['userpassword']
            }


@api.route("/")
@api.route("/index")
def index():
    return render_template("index.html")


@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

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
        return render_template("create_account.html")

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
    return render_template("profile.html")


@api.route("/admin")
@logged_in
@is_admin
def admin():
    # TODO: add middleware function to make sure that a user must be logged
    #       in to see this page, and that they can only see their page
    return render_template("admin.html")


@api.errorhandler(404)
def not_found(e):
    return render_template("error.html")


if __name__ == '__main__':
    # put all "to be run"
    api.run()
    # api.run(host='0.0.0.0', debug=False, port=os.environ.get('PORT', 80))

def setupApp():
    return 0
