# Flask/DB Imports
from flask import Flask, request, redirect, url_for, session, render_template
from flask_cors import CORS
from flask_session import Session
from sqlalchemy import create_engine, Table, MetaData
import cymysql

# Non Flask/DB imports
import json
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


# list of columns in DB
# users - userid [INT]; username [string 45]; userpassword [string 45]; isadmin [1 is true, 0 is false]
# lists - primarylistid [INT]; listid [INT]; userid [INT]; itemid [INT]; itemposition [INT]; priority [1 is true, 0 is false]
# items - itemid [INT]; url [string 500]; description [string 500]; imageurl [string 500]; title [string 100]
# all DB query calls can be referenced here https://flask.palletsprojects.com/en/1.1.x/patterns/sqlalchemy/

def _session_create(username, is_admin, user_id):
    session["user"] = username
    session["is_admin"] = is_admin
    session["user_id"] = user_id


def _session_destroy():
    session.pop("user", None)
    session.pop("is_admin", None)
    session.pop("user_id", None)


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
    messages = request.args.get("messages", None)
    return render_template("index.html", messages=messages)


# ------------------------------------- Account Related Routes -------------------------------------

@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    # POST
    else:
        username = request.form.get("user")
        password = request.form.get("pass")

        if username == "user_in_db":
            _session_create(username, False, 0)
            return redirect(url_for("profile"))

        else:
            return render_template("login.html", login_failed=True, message="Username and Password not found!")


@api.route('/logout')
def logout():
    _session_destroy()
    return redirect(url_for('index', messages={"logout": "Successful"}))


@api.route("/account/create", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return render_template("create_account.html")

    # POST
    else:
        username = request.form.get("user")
        email = request.form.get("email")
        password = request.form.get("pass")

        if username != "user_in_db":
            _session_create(username, False, 0)
            return redirect(url_for("profile"))

        else:
            return render_template("login.html", create_failed=True, message=f"Username: {username} is already taken!")


@api.route("/profile", methods=["GET", "PUT", "DELETE"])
@logged_in
def profile():
    if request.method == "GET":
        list_modified = request.args.get("list_modified", None)

        return render_template("profile.html", list_modified=list_modified, user={"username": "user1",
                                                                                  "email": "user1@gmail.com",
                                                                                  "password": "password",
                                                                                  "wishlists": [
                                                                                      {"name": "list1", "num_items": 5,
                                                                                       "list_id": 1},
                                                                                      {"name": "list2", "num_items": 10,
                                                                                       "list_id": 2},
                                                                                      {"name": "list3", "num_items": 2,
                                                                                       "list_id": 3},
                                                                                  ]})

    elif request.method == "PUT":
        username = request.form.get("user")
        email = request.form.get("email")
        password = request.form.get("pass")

        successes = {
            "username": True if username is not None and username != "user_in_db" else False,
            "email": True if email is not None else False,
            "password": True if password is not None else False,
        }

        return render_template("profile.html", user={"username": "user1",
                                                     "email": "user1@gmail.com",
                                                     "password": "password",
                                                     "wishlists": [
                                                         {"name": "list1", "num_items": 5, "list_id": 1},
                                                         {"name": "list2", "num_items": 10, "list_id": 2},
                                                         {"name": "list3", "num_items": 2, "list_id": 3},
                                                     ]},
                               successes=successes)

    # DELETE
    else:
        return url_for("index", messages={"Delete Account": "Successful"})


# ------------------------------------- Wishlist Related Routes -------------------------------------

@api.route("/wishlist/<list_id>")
def view_wishlist(list_id):
    item_modified = request.args.get("item_modified", None)

    return render_template("wishlist.html", item_modified=item_modified, wishlist={
        "name": "list1",
        "id": 1,
        "items": [
            {"id": 1, "title": "item1", "url": "https://foo.com", "image_url": "https://foo.png", "position": 3,
             "priority": 0},
            {"id": 2, "title": "item2", "url": "https://bar.com", "image_url": "https://bar.png", "position": 1,
             "priority": 1},
            {"id": 3, "title": "item3", "url": "https://baz.com", "image_url": "https://baz.png", "position": 2,
             "priority": 1}
        ]
    })


@api.route("/wishlist/<list_id>", methods=["PUT", "POST", "DELETE"])
@logged_in
def modify_wishlist(list_id):
    if request.method == "PUT":
        return render_template("wishlist.html", list_put=True, wishlist={
            "name": "list1",
            "id": 1,
            "items": [
                {"id": 1, "title": "item1", "url": "https://foo.com", "image_url": "https://foo.png", "position": 3,
                 "priority": 0},
                {"id": 2, "title": "item2", "url": "https://bar.com", "image_url": "https://bar.png", "position": 1,
                 "priority": 1},
                {"id": 3, "title": "item3", "url": "https://baz.com", "image_url": "https://baz.png", "position": 2,
                 "priority": 1}
            ]
        })

    elif request.method == "POST":
        return redirect(url_for("profile.html", list_modified={"id": 3, "action": "added", "success": True}))

    # DELETE
    else:
        return redirect(url_for("profile.html", list_modified={"id": 3, "action": "deleted", "success": True}))


# ------------------------------------- Item Related Routes -------------------------------------

@api.route("/wishlist/<list_id>/<item_id>")
def view_wishlist_item(list_id, item_id):
    return render_template("wishlist_item.html", wishlist={
        "list_id": 1,
        "item": {"id": 1, "title": "item1", "url": "https://foo.com", "image_url": "https://foo.png", "position": 3,
                 "priority": 0}
    })


@api.route("/wishlist/<list_id>/<item_id>", methods=["PUT", "POST", "DELETE"])
@logged_in
def modify_wishlist_item(list_id, item_id):
    if request.method == "PUT":
        return render_template("wishlist_item.html", item_put=True, wishlist={
            "list_id": 1,
            "item": {"id": 1, "title": "item1", "url": "https://foo.com", "image_url": "https://foo.png", "position": 3,
                     "priority": 0}
        })

    elif request.method == "POST":
        return redirect(
            url_for("/wishlist", list_id=list_id, list_modified={"id": 3, "action": "added", "success": True}))

    # DELETE
    else:
        return redirect(
            url_for("/wishlist", list_id=list_id, list_modified={"id": 3, "action": "deleted", "success": True}))


# ------------------------------------- Admin Related Routes -------------------------------------

@api.route("/admin")
@logged_in
@is_admin
def admin():
    return render_template("admin.html", users=[
        {"username": "user1", "email": "user1@gmail.com", "password": "password"},
        {"username": "user2", "email": "user2@gmail.com", "password": "password"},
        {"username": "user3", "email": "user3@gmail.com", "password": "password"},
        {"username": "user4", "email": "user4@gmail.com", "password": "password"},
    ])


@api.errorhandler(404)
def not_found(e):
    return render_template("error.html")


if __name__ == '__main__':
    # put all "to be run"
    api.run()
