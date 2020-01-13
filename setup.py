#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from app_template import create_app
from app_template.extensions import db, ma
from app_template.models import User, Links, Tasks, TasksSchema


app = create_app()


@app.shell_context_processor
def make_shell_context():
    """ To work with the application in the terminal.
        Helps not create module imports manually.
        To start, run the commands in terminal:
        $ export FLASK_APP=setup.py
        $ flask shell
        Simple example:
        >>>db
        <SQLAlchemy engine=sqlite:////path_to_db/......
        >>>Example
        <class 'app_template.models.Example'> """
    return {
        'db': db,
        'ma': ma,
        'User': User,
        'Links': Links,
        'Tasks': Tasks,
        'TasksSchema': TasksSchema
        }  # Add more variables {name:variable}


# TODO: start app: $ python3 setup.py OR $ flask run
if __name__ == "__main__":
    app.run(host='0.0.0.0')
