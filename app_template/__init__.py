#! /usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'MOIS3Y'

from flask import Flask, current_app
from config import Config, DevelopmentConfig  # noqa: F401
from commands import create_users, create_tasks, create_links
from .extensions import db, migrate, ma, guard, csrf, login


# *Create Flask app
def create_app(config_class=DevelopmentConfig):  # ! OR Config for production
    app = Flask(__name__)
    app.config.from_object(config_class)

    # *Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    guard.init_app(app, User)
    csrf.init_app(app)
    login.init_app(app)

    # *Add click commands
    app.cli.add_command(create_users)
    app.cli.add_command(create_tasks)
    app.cli.add_command(create_links)

    # Main Blueprint
    from app_template.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Auth Blueprint
    from app_template.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    # CORS Blueprint
    from app_template.cors import bp as cors_bp
    app.register_blueprint(cors_bp, url_prefix='/cors')

    # API Blueprint
    from app_template.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # *Exclude all the views of a blueprint from protection CSRF
    csrf.exempt(api_bp)

    # *Add context to base.html
    @app.context_processor
    def inject_to_base_html():
        links = Links.query.all()
        return dict(current_app=current_app, links=links)

    return app


from .models import User, Links  # noqa E402;F401