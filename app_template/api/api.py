from flask import jsonify, abort, make_response, request, url_for
from flask_praetorian import auth_required

from app_template.extensions import db, guard
from app_template.models import Tasks, TasksSchema, User
from ..api import bp


def make_public_task(task):
    """ change id to uri """

    url_task = {}
    for field in task:
        if field == 'id':
            url_task['uri'] = url_for(
                'api.get_task', task_id=task['id'], _external=True)
        else:
            url_task[field] = task[field]
    return url_task


# * curl -i http://localhost:5000/api/v.1.0/todo/tasks
@bp.route('/v.1.0/todo/tasks', methods=['GET'])
def get_tasks():
    response = []
    tasks = Tasks.query.all()
    if tasks:
        # class serialization in JSON
        tasks = TasksSchema().dump(tasks, many=True)
        for task in tasks:
            response.append(make_public_task(task))
    else:
        response = 'no tasks'

    return jsonify({'tasks': response})


# * curl -i http://localhost:5000/api/v.1.0/todo/tasks/1 or 2,3....
@bp.route('/v.1.0/todo/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Tasks.query.get(task_id)
    if task:
        # class serialization in JSON
        task = TasksSchema().dump(task)
        response = make_public_task(task)

        return jsonify({'task': response})
    abort(404)


# * curl -i -H "Content-Type: application/json" -X POST
# * -d '{"title":"Read a book"}' http://localhost:5000/api/v.1.0/todo/tasks
@bp.route('/v.1.0/todo/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    new_task = Tasks(
        title=request.json['title'],
        description=request.json.get('description', ""))

    db.session.add(new_task)
    db.session.commit()

    last_task = Tasks.query.order_by(Tasks.id.desc()).first()
    if last_task:
        # class serialization in JSON
        task = TasksSchema().dump(last_task)
        response = make_public_task(task)
    return jsonify({'new_task': response}), 201


# * curl -i -H "Content-Type: application/json" -X PUT
# * -d '{"done":true}' http://localhost:5000/api/v.1.0/todo/tasks/2
@bp.route('/v.1.0/todo/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(
            request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task = Tasks.query.get(task_id)
    if task:
        task.title = request.json.get('title', task.title)
        task.description = request.json.get('description', task.description)
        task.done = request.json.get('done', task.done)

        db.session.add(task)
        db.session.commit()
        # class serialization in JSON
        task = TasksSchema().dump(task)
        response = make_public_task(task)
        return jsonify({'task_update': response})
    abort(404)


# * curl -i -H "Content-Type: application/json" -X DELETE
# * http://localhost:5000/api/v.1.0/todo/tasks/2
@bp.route('/v.1.0/todo/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Tasks.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        response = {'task_delete': 'Success'}
        return jsonify(response)
    abort(404)


@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


# ! GUARD API

# * curl -i -H "Content-Type: application/json" -X POST
# * -d '{"username":"One", "password":"one"}' http://localhost:5000/api/login
@bp.route('/login', methods=['POST'])
def login():
    if not request.json:
        abort(400)
    if 'username' not in request.json or 'password' not in request.json:
        abort(400)

    user = User.query.filter_by(username=request.json['username']).first()
    if user is None or not user.check_password_hash(request.json['password']):
        abort(401)

    token = guard.encode_jwt_token(user)
    return jsonify({'access_token': token})


# * curl -i -X GET -H "Authorization: Bearer <your token>"
# * http://localhost:5000/api/protected
@bp.route('/protected')
@auth_required
def protected():
    return jsonify({'result': 'You are in a special area!'})


# * curl -i -H "Content-Type: application/json" -X POST
# * -d '{"token":"<your token>"}' http://localhost:5000/api/refresh
@bp.route('/refresh', methods=['POST'])
def refresh():
    token = guard.refresh_jwt_token(request.json['token'])
    return jsonify({'update_token': token})


# * Test route
@bp.route('/open')
def open():
    return jsonify({'result': 'Hello, friend'})
