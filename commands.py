import click
from flask.cli import with_appcontext

from app_template.extensions import db
from app_template.models import User, Tasks, Links


@click.command(name='create_database')
@with_appcontext
def create_database():
    db.create_all()


@click.command(name='create_users')
@with_appcontext
def create_users():
    one = User(username='One')
    one.set_password('one')
    print(one.__repr__())
    two = User(username='Two')
    two.set_password('two')
    print(two.__repr__())
    three = User(username='Three')
    three.set_password('three')
    print(three.__repr__())
    # two = User(username='Two', password=guard.hash_password('two'))
    # three = User(username='Three', password=guard.hash_password('three'))

    db.session.add_all([one, two, three])
    db.session.commit()


@click.command(name='create_tasks')
@with_appcontext
def create_tasks():
    first = Tasks(
        title='create main Blueprint',
        description='add frontend',
        done=False)
    second = Tasks(
        title='create cors Blueprint',
        description='add local page',
        done=False)
    third = Tasks(
        title='create api Blueprint',
        description='add db fields',
        done=False)

    db.session.add_all([first, second, third])
    db.session.commit()


@click.command(name='create_links')
@with_appcontext
def create_links():
    flask_doc = Links(
        name_url='Flask microframework',
        url='http://flask.palletsprojects.com/en/1.1.x/')
    sqlachemy = Links(
        name_url='Flask SqlAlchemy',
        url='https://flask-sqlalchemy.palletsprojects.com/en/2.x/')
    migrate = Links(
        name_url='Flask Migrate',
        url='https://flask-migrate.readthedocs.io/en/latest/')
    login = Links(
        name_url='Flask Login',
        url='https://flask-login.readthedocs.io/en/latest/')
    cors = Links(
        name_url='Flask CORS',
        url='https://flask-cors.readthedocs.io/en/latest/')
    wtf = Links(
        name_url='Flask WTF',
        url='https://flask-wtf.readthedocs.io/en/stable/')

    db.session.add_all([flask_doc, sqlachemy, migrate, login, cors, wtf])
    db.session.commit()
