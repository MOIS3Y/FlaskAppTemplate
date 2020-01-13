from .extensions import db, ma


class Tasks(db.Model):
    """ Test database model. Create your models."""

    tasks = [
        {
            'id': 1,
            'title': 'Buy groceries',
            'description': 'Milk, Cheese, Pizza, Fruit, Tylenol',
            'done': False
        },
        {
            'id': 2,
            'title': 'Learn Python',
            'description': 'Need to find a good Python tutorial on the web',
            'done': False}
    ]
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    description = db.Column(db.String(150))
    done = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        """ This method tells Python how to print objects of this class """
        return '<Task: {}>'.format(self.title)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.Text)

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.filter_by(id=id).one_or_none()

    @property
    def rolenames(self):
        return []

    @property
    def identity(self):
        return self.id

    def __repr__(self):
        """ This method tells Python how to print objects of this class """
        return '<User: {}>'.format(self.username)


class Links(db.Model):
    """ Test database model. Create your models.
        It just keeps a link to the documentation.
        And created to demonstrate how you can easily put data
        from a db into a base.html """

    application_name = 'app_template'
    id = db.Column(db.Integer, primary_key=True)
    name_url = db.Column(db.String(50))
    url = db.Column(db.Text)

    def __repr__(self):
        """ This method tells Python how to print objects of this class """
        return '<Link: {}>'.format(self.name_url)


# *Marshmellow Schemes
class TasksSchema(ma.ModelSchema):
    """ Class serialization in JSON """
    class Meta:
        model = Tasks


__doc__ = """
#TODO: SQLAlchemy prompt:
    Official documentation:
        https://flask-sqlalchemy.palletsprojects.com/en/2.x/

    Integer      --- an integer.
    String(size) --- a string with a maximum length.
    Text         --- some longer unicode text.
    DateTime     --- date and time expressed as Python datetime object.
    Float        --- stores floating point values
    Boolean      --- stores a boolean value
    PickleType   --- stores a pickled Python object
    LargeBinary  --- stores large arbitrary binary data


# ? Simple Example Create Class:
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)

        def __repr__(self):
            return '<User {}>'.format(self.username)

# ? One-to-Many Relationships:

    class Person(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(50), nullable=False)
        addresses = db.relationship('Address', backref='person', lazy=True)

    class Address(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), nullable=False)
        person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
            nullable=False)

    Notes:
        db.relationship() - who owns the address (Person)
            If you would want to have a one-to-one relationship
            you can pass uselist=False to relationship().

        db.ForeignKey('person.id') - class relationship key

        nullable=False - tells SQLAlchemy to create the column as NOT NULL

        backref='person' - declare a new property on the Address class:
            my_address.person
            my_address.person.name

        lazy=... defines when SQLAlchemy will load the data from the database:
            read more in documentation

# ? Many-to-Many Relationships
    If you want to use many-to-many relationships
    you will need to define a helper table that is used for the relationship.
    For this helper table it is strongly recommended to not use a model
    but an actual table:

    tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True
    ))

    class Page(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        tags = db.relationship('Tag', secondary=tags, lazy='subquery',
            backref=db.backref('pages', lazy=True))

    class Tag(db.Model):
        id = db.Column(db.Integer, primary_key=True)

# ? Select, Insert, Delete
    1.Inserting data into the database is a three step process:
    2.Create the Python object
    3.Add it to the session
    4.Commit the session

    # * Inserting:
    >>> from yourapp import User
    >>> me = User('admin', 'admin@example.com')

    >>> db.session.add(me)
    >>> db.session.commit()
    >>> me.id
    1
    # ! Deleting records is very similar, instead of add() use delete():
    >>> db.session.delete(me)
    >>> db.session.commit()

    # * Querying Records:
    # ! Get All:
    get_data_db = Class_name.query.all()
    # ! Ordering by something:
    get_data_db = Class_name.query.order_by(Class.field).all()
    # ! Retrieve first by filter:
    get_data_db = Class_name.query.filter_by(field='example').first()
    get_data_db = Class_name.query.filter(Class.field.endswith('.com')).all
    # ! Limiting:
    get_data_db = Class_name.query.limit(1).all()
    # ! Getting user by primary key:
    get_data_db = Class_name.query.get(№)
    # ! Queries in Views:
    get_data_db = Class_name.query.filter_by(field='example').first_or_404()

    More good examples in documentation.....


#TODO: Migrate prompt:

To create repository migration, run the commands in terminal:
    $ export FLASK_APP=setup.py

    $ flask db init
    $ flask db migrate -m "your message"
    $ flask db upgrade

"""
