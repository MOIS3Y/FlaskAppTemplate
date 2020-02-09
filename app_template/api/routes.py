from flask import (
    jsonify,
    abort,
    make_response,
    request,
    url_for,
    render_template)
from flask_praetorian import auth_required, current_user, roles_required

from app_template.extensions import db, guard
from app_template.models import Tasks, TasksSchema, User
from ..api import bp


def make_public_task(tasks):
    """
    This is a helper function.
    Prepares a class 'Tasks' for serialization in JSON
    Using a nested function 'pretty_task()'
    hides the internal structure API from the user
    and makes the output of information more beautiful.
    """
    def pretty_task(task):
        """
        This is a nested functions.
        It changes the task id to the url task path.
        Deletes the user id field.
        """

        pretty_task = {}
        for field in task:
            if field == 'id':
                # ? Replace id task to uri
                pretty_task['uri'] = url_for(
                    'api.get_task', task_id=task['id'], _external=True)
            # ? Delete user id
            elif field == 'user':
                continue
            else:
                pretty_task[field] = task[field]
        return pretty_task

    if tasks:
        if type(tasks) == list:
            public_tasks = []
            # ? class serialization in JSON
            tasks = TasksSchema().dump(tasks, many=True)
            for task in tasks:
                public_tasks.append(pretty_task(task))
            return public_tasks
        else:
            # ? class serialization in JSON
            task = TasksSchema().dump(tasks)
            public_task = pretty_task(task)
            return public_task


# ! API Routes


@bp.route('/v.1.0/ping', methods=['GET'])
def ping():
    """ Test route """
    return jsonify({'response': 'Hello, friend'})


@bp.route('/v.1.0/protected', methods=['GET'])
@auth_required
def protected():
    """
    Test route to verify the health of the application’s protection.
    Returns current user data. To access, you need to go through verification
    and get a token. With each request it is necessary to transfer a token in
    the request header.

    A simple request example:

    curl
    -i -X GET
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <your token>"
    http://localhost:5000/api/v.1.0/protected
    """

    return jsonify(
        {
            'result': 'You are in a special area!',
            'your_id': current_user().id,
            'your_name': current_user().username
        })


@bp.route('/v.1.0/todo/tasks', methods=['GET'])
@auth_required
def get_tasks():
    """
    Generates a list of user tasks.
    To access, you need to go through verification and get a token.
    With each request it is necessary to transfer a token in the request
    header. Based on this, the current user is determined and a database
    query is made.

    A simple request example:

    curl
    -i -X GET
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <your token>"
    http://localhost:5000/api/v.1.0/todo/tasks

    """
    user = current_user()
    tasks = Tasks.query.filter_by(user_id=user.id).all()
    response = make_public_task(tasks)
    if response:
        return jsonify({'tasks': response})
    else:
        return jsonify({'tasks': 'no tasks'})


@bp.route('/v.1.0/todo/tasks/<int:task_id>', methods=['GET'])
@auth_required
def get_task(task_id):
    """
    Gets the user task.
    To access, you need to go through verification and get a token.
    With each request it is necessary to transfer a token in the request
    header. Based on this, the current user is determined and a database
    query is made.

    A simple request example:

    curl
    -i -X GET
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <your token>"
    http://localhost:5000/api/v.1.0/todo/tasks/1 or 2,3....

    """
    user = current_user()
    task = Tasks.query.filter_by(user_id=user.id, id=task_id).first()
    response = make_public_task(task)
    if response:
        return jsonify({'task': response})

    abort(404)


@bp.route('/v.1.0/todo/tasks/new', methods=['POST'])
@auth_required
def create_task():
    """
    Creates a new task.
    To access, you need to go through verification and get a token.
    With each request it is necessary to transfer a token in the request
    header. Based on this, the current user is determined, a task is created,
    and a database query is made.
    Mandatory field is the "title". Default 'done'=False

    A simple request example:

    curl
    -i -X POST
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <your token>"
    -d '{"title":"Read a book"}'
    http://localhost:5000/api/v.1.0/todo/tasks/new

    """

    user = current_user()
    if not request.json or 'title' not in request.json:
        abort(400)
    new_task = Tasks(
        title=request.json['title'],
        description=request.json.get('description', ""),
        user_id=user.id)
    # *Add to db new task
    db.session.add(new_task)
    db.session.commit()
    # *Get from db new task
    last_task = Tasks.query.filter_by(user_id=user.id).order_by(
        Tasks.id.desc()).first()
    # *Show new task
    response = make_public_task(last_task)
    if response:
        return jsonify({'new_task': response}), 201


@bp.route('/v.1.0/todo/tasks/<int:task_id>', methods=['PUT'])
@auth_required
def update_task(task_id):
    """
    Updates a task.
    To access, you need to go through verification and get a token.
    With each request it is necessary to transfer a token in the request
    header. Based on this, the current user is determined and a database
    query is made.
    Request verification - checks the request fields.Ignores extra fields
    that are not defined in the "Tasks" class.

    A simple request example:

    curl
    -i -X PUT
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <your token>"
    -d '{"done":true}'
    http://localhost:5000/api/v.1.0/todo/tasks/2

    """

    user = current_user()
    # * Request verification
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(
            request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    task = Tasks.query.filter_by(user_id=user.id, id=task_id).first()
    # * Change task
    if task:
        task.title = request.json.get('title', task.title)
        task.description = request.json.get('description', task.description)
        task.done = request.json.get('done', task.done)

        db.session.add(task)
        db.session.commit()
        response = make_public_task(task)
        return jsonify({'task_update': response})

    abort(404)


@bp.route('/v.1.0/todo/tasks/<int:task_id>', methods=['DELETE'])
@auth_required
def delete_task(task_id):
    """
    Deletes a task.
    To access, you need to go through verification and get a token.
    With each request it is necessary to transfer a token in the request
    header. Based on this, the current user is determined and a database
    query is made.

    A simple request example:

    curl
    -i -X DELETE
    -H "Content-Type: application/json"
    -H "Authorization: Bearer <your token>"
    http://localhost:5000/api/v.1.0/todo/tasks/1 or 2,3....

    """

    user = current_user()
    task = Tasks.query.filter_by(user_id=user.id, id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        response = {'task_delete': 'Success'}
        return jsonify(response)

    abort(404)


# ! API Admin routes


@bp.route('/v.1.0/admin/todo/tasks/<username>', methods=['GET'])
@roles_required('admin')
def get_user_tasks(username):
    user = User.query.filter_by(username=username).first()
    if user:
        tasks = Tasks.query.filter_by(user_id=user.id).all()
        response = make_public_task(tasks)
        if response:
            return jsonify({'tasks': response})
        else:
            return jsonify({'tasks': 'no tasks'})
    abort(404)


# ! GUARD API


@bp.route('/v.1.0/login', methods=['POST'])
def login():
    """
    Creates a temporary token for a registered user.
    To create a token, you need to send a json request
    containing the user name and password. To access all protected routes,
    (@auth_required) you need to add the received token in the header.
    Token lifetime is configured in the config.py
    (JWT_ACCESS_LIFESPAN = {'minutes': 20})

    A simple request example:

    curl
    -i -X POST
    -H "Content-Type: application/json"
    -d '{"username":"One", "password":"one"}'
    http://localhost:5000/api/v.1.0/login
    """

    if not request.json:
        abort(400)
    if 'username' not in request.json or 'password' not in request.json:
        abort(400)

    user = User.query.filter_by(username=request.json['username']).first()
    if user is None or not user.check_password_hash(request.json['password']):
        abort(401)

    token = guard.encode_jwt_token(user)
    return jsonify({'access_token': token})


@bp.route('/v.1.0/refresh', methods=['POST'])
def refresh():
    """
    Updates the token if its lifetime has expired.
    Updates the token if its lifetime has expired.
    To get a new token, you need to send the old token in the POST request

    A simple request example:

    curl
    -i -X POST
    -H "Content-Type: application/json"
    -d '{"token":"<your token>"}'
    http://localhost:5000/api/v.1.0/refresh
    """

    token = guard.refresh_jwt_token(request.json['token'])
    return jsonify({'update_token': token})


# ! Web routes


@bp.route('/', methods=['GET'])
def index():
    return render_template('api/index.html', title='API Blueprint')


# ! Customization of standard error output


@bp.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@bp.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)
