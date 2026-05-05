from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.est_admin:
            flash('Acces reserve aux administrateurs.', 'danger')
            return redirect(url_for('membres.dashboard'))
        return f(*args, **kwargs)
    return decorated_function


def admin_ou_secretaire_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.est_membre:
            flash('Acces non autorise.', 'danger')
            return redirect(url_for('membres.dashboard'))
        return f(*args, **kwargs)
    return decorated_function