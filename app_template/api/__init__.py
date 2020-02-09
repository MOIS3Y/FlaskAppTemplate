from flask import Blueprint


bp = Blueprint('api', __name__, template_folder='templates')


from ..api import routes # noqa E402;F401