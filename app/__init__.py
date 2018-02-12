# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect
from config import Config

db = SQLAlchemy(session_options={'autocommit': False,
                                         'autoflush': False,})
db.Model.__table_args__ = {
    'mysql_engine': 'InnoDB',
    'mysql_charset': 'utf8'
}


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # # csrf protection
    # csrf = CsrfProtect()
    # csrf.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


