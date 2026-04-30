import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix

DB = SQLAlchemy()
LOGIN_MANAGER = LoginManager()
LIMITER = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:////tmp/healthcare.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    DB.init_app(app)
    LOGIN_MANAGER.init_app(app)
    LIMITER.init_app(app)
    LOGIN_MANAGER.login_view = "main.login"

    from app.models import User

    @LOGIN_MANAGER.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        DB.create_all()
    return app
