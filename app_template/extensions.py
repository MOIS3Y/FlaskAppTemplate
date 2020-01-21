from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_praetorian import Praetorian
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# *SQL DataBase
db = SQLAlchemy()
migrate = Migrate()


# *Marshmallow /Converting Flask-SQLAlchemy to JSON/
ma = Marshmallow()


# *Login Manager
login = LoginManager()


# *GUARD App
guard = Praetorian()
csrf = CSRFProtect()
