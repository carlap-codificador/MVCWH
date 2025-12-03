# decorators.py
from functools import wraps
from flask import session, redirect, url_for, request

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            # si no está logueado, se va a login
            return redirect(url_for("login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function
