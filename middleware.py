from functools import wraps
from flask import Response, session


def logged_in(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "user" in session:
            return func(*args, **kwargs)

        return Response("No user logged in", mimetype="text/plain", status=403)

    return decorated_function


def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if session["is_admin"]:
            return func(*args, **kwargs)

        return Response("Admin not logged in", mimetype="text/plain", status=403)

    return decorated_function
