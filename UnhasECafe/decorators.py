from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def check_is_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("Por favor, faça login primeiro.", "warning")
            return redirect(url_for("login"))
        if not current_user.confirmado:
            flash("Por favor, confirme sua conta!", "warning")
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    return decorated_function
