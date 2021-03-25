# Flask/DB Imports
from flask import Flask, request, redirect, url_for, session, render_template
from sqlalchemy.sql.elements import Null
from sqlalchemy.sql.selectable import Select
from werkzeug.datastructures import TypeConversionDict
from flask_cors import CORS
from flask_session import Session
from sqlalchemy import create_engine, Table, MetaData, insert, delete, update
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

con = engine.connect()

# list of columns in DB
# users - userid [INT]; username [string 45]; email [string 200]; userpassword [string 45]; isadmin [1 is true, 0 is false]
# lists - primarylistid [INT]; listname [string 100]; userid [INT]; itemid [INT]; itemposition [INT]; priority [1 is true, 0 is false]
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

def item_serialize(item_id):
    item = items.select(items.c.itemid==item_id).execute().first()
    return { 
                "item": item['itemid'],
                "title" : item['title'], 
                "description": item['description'],
                "url": item['url'],
                "image": item['imageurl']
            }

def list_serializer():
    user = users.select(users.c.userid == session['user_id']).execute().first()
    userlist = lists.select(lists.c.userid == session['user_id']).execute().all()
        
    # list = pk, name, user id, item id, item position, priority
    itemlist = []
    for obj in userlist:
        item = item_serialize(obj['itemid'])

        itemlist.append(item)

    return { "user" : user, "user_list" : userlist, "item_list" : itemlist }


@api.route("/time")
def get_current_time():
    return {
        "time": time.time(),
        "user1": 'userpassword'
            }


@api.route("/")
@api.route("/index")
def index():
    messages = request.args.get("messages", None)
    return render_template("index.html", messages=messages)


# ------------------------------------- Account Related Routes -------------------------------------

@api.route("/login", methods=["GET", "POST"])
def login():
    login_page = "login.html"
    if request.method == "GET":
        return render_template(login_page)

    # POST
    else:
        username = request.form.get("user")
        password = request.form.get("pass")

        try:
            user = users.select(users.c.username == username and users.c.userpassword == password).execute().first()
        except Exception:
            print(Exception)

        if user != None:
            _session_create(user['username'], user['isadmin'] == 1, user['userid'])
            return redirect(url_for("profile"))

        else:
            return render_template(login_page, login_failed=True, message="Username and Password not found!")


@api.route('/logout')
def logout():
    _session_destroy()
    return redirect(url_for('index', messages={"logout": "Successful"}))


@api.route("/account/create", methods=["GET", "POST"])
def create_account():
    if request.method == "GET":
        return render_template("create_account.html")

    # POST
    # We never get here atm
    else:
        new_username = request.form.get("user")
        new_email = request.form.get("email")
        new_password = request.form.get("pass")

        user = users.select(users.c.username == new_username and users.c.userpassword == new_password and users.c.email == new_email).execute().first()

        con.execute(users.insert(), username=new_username, userpassword=new_password, email=new_email, isadmin=0)

        if user != None:
            _session_create(user['username'], user['isadmin'] == 1, user['userid'])
            return redirect(url_for("profile"))

        else:
            return render_template("create_account.html", create_failed=True, message=f"Username: {new_username} is already taken!")


@api.route("/profile", methods=["GET", "PUT", "DELETE"])
@logged_in
def profile():
    if request.method == "GET":
        list_modified = request.args.get("list_modified", None)
        
        list_serialized = list_serializer()
        
            
        return render_template("profile.html", list_modified=list_modified, user={
                                                                "username": list_serialized['user']['username'], 
                                                                "password": list_serialized['user']['userpassword'],
                                                                "email": list_serialized['user']['email'], 
                                                                "wishlist_name": list_serialized['user_list'][0]['listname'],
                                                                "wishlist": list_serialized['item_list']
                                                                })

    elif request.method == "PUT":
        new_username = request.form.get("user")
        new_email = request.form.get("email")
        new_password = request.form.get("pass")

        successes = {
            "username": True if new_username is not None else False,
            "email": True if new_email is not None else False,
            "password": True if new_password is not None else False,
        }

        users.update().where(users.c.userid==session['user_id']).values(username=new_username, email=new_email, userpassword=new_password).execute()

        list_serialized = list_serializer()

        return render_template("profile.html", user={
                                                    "username": list_serialized['user']['username'], 
                                                    "password": list_serialized['user']['userpassword'],
                                                    "email": list_serialized['user']['email'], 
                                                    "wishlist_name": list_serialized['user_list'][0]['listname'],
                                                    "wishlist": list_serialized['item_list'] 
                                                    }, successes=successes)

    # DELETE
    else:
        users.delete().where(users.c.userid==session['user_id']).execute()
        _session_destroy()
        return url_for("index", messages={"Delete Account": "Successful"})


# ------------------------------------- Wishlist Related Routes -------------------------------------

@api.route("/wishlist/<list_id>")
def view_wishlist(list_id):
    item_modified = request.args.get("item_modified", None)

    list_serialized = list_serializer()

    return render_template("wishlist.html", item_modified=item_modified, wishlist={
        "name": list_serialized['user_list'][0]['listname'],
        "id": session['user_id'],
        "items": list_serialized['item_list']
    })


@api.route("/wishlist/<list_id>", methods=["PUT", "POST", "DELETE"])
@logged_in
def modify_wishlist(list_id):
    list_serialized = list_serializer()
    if request.method == "PUT":
        #UPDATE ITEM

        return render_template("wishlist.html", list_put=True, wishlist={
            "name": list_serialized['user_list'][0]['listname'],
            "id": session['user_id'],
            "items": list_serialized['item_list']
            })

    elif request.method == "POST":
        #ADD ITEM
        return redirect(url_for("profile", list_modified={"id": 3, "action": "added", "success": True}))

    # DELETE
    else:
        #DELETE ITEM
        return redirect(url_for("profile", list_modified={"id": 3, "action": "deleted", "success": True}))


# ------------------------------------- Item Related Routes -------------------------------------

@api.route("/wishlist/<item_id>")
def view_wishlist_item(item_id):

    this_item = item_serialize(item_id)
    user_list = list_serializer()

    #TESTING
    print(this_item)
    print(user_list)

    return render_template("wishlist_item.html", wishlist={
        "list_id": user_list['user']['userid'],
        "item": this_item
    })


@api.route("/wishlist/<item_id>", methods=["PUT", "POST", "DELETE"])
@logged_in
def modify_wishlist_item(item_id):
    if request.method == "PUT":
        # UPDATE ITEM

        return render_template("wishlist_item.html", item_put=True, wishlist={
            "list_id": 1,
            "item": {"id": 1, "title": "item1", "url": "https://foo.com", "image_url": "https://foo.png", "position": 3,
                     "priority": 0}
        })

    elif request.method == "POST":

        # ADD A ITEM

        return redirect(
            url_for("view_wishlist", list_id=session['user_id'], list_modified={"id": 3, "action": "added", "success": True}))

    # DELETE
    else:
        #DELETE ITEM

        return redirect(
            url_for("view_wishlist", list_id=session['user_id'], list_modified={"id": 3, "action": "deleted", "success": True}))


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