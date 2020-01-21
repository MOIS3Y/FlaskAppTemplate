from flask import render_template

from ..api import bp


@bp.route('/', methods=['GET'])
def index():
    return render_template('api/index.html', title='API Blueprint')
