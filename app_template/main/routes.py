from flask import render_template
from app_template.main import bp
from app_template.models import Links


# *Test route http//:localhost:5000/ OR http//:localhost:5000/index
@bp.route('/')
@bp.route('/index', methods=['GET'])
def index():
    get_links = Links.query.all()

    return render_template(
        'main/index.html',
        title='Main Blueprint',
        application_name=Links.application_name,
        links=get_links)
