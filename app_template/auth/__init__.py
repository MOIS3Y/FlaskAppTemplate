from flask import Blueprint


bp = Blueprint('auth', __name__, template_folder='templates')


from ..auth import auth  # noqa E402;F401