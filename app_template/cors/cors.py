import os
from flask import render_template, jsonify
from flask_cors import cross_origin
from app_template.cors import bp
from app_template.models import Links


# *http://localhost:5000/cors
@bp.route('/', methods=['GET'])
def index():
    get_links = Links.query.all()
    BLUEPRINT_ROOT = os.path.realpath(os.path.dirname(__file__))
    cors_page_url = os.path.join(BLUEPRINT_ROOT, 'templates/cors', 'cors.html')

    return render_template(
        'cors/index.html',
        application_name=Links.application_name,
        links=get_links,
        cors_page_url=cors_page_url)


@bp.route('/pong', methods=['GET'])
# ! This is not a safe method. Read more in documentation.
# ! Use the filter of those who have access to CORS requests.
# ? @cross_origin(origins=[r"http://192.168.1.99/*", ...)
@cross_origin()
def ping_pong():
    return jsonify('Pong!')
