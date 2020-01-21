from flask import render_template
from app_template.main import bp


# *Test route http//:localhost:5000/ OR http//:localhost:5000/index
@bp.route('/')
@bp.route('/index', methods=['GET'])
def index():
    return render_template('main/index.html', title='Main Blueprint')
