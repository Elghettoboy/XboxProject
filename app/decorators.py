from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Si el usuario actual no tiene el campo is_admin en True...
        if not current_user.is_admin:
            # ...le mostramos un error 403 (Acceso Prohibido).
            abort(403)
        # Si es admin, dejamos que la función original (la vista) se ejecute.
        return f(*args, **kwargs)
    return decorated_function

