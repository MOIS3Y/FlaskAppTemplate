from flask import Blueprint


bp = Blueprint('cors', __name__, template_folder='templates')


from ..cors import cors  # noqa:E402, F401
