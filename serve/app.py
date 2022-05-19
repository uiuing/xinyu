from flask import Flask
from flask_cors import CORS

from model.user import db
from router import sign, content, message


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    CORS(app, supports_credentials=True)

    app.config.from_pyfile('config.py')
    app.config.from_object('config.SQLALCHEMY_DATABASE_URI')

    # 登录注册的路由
    app.register_blueprint(sign.sign, url_prefix='/sign')
    app.register_blueprint(content.content, url_prefix='/content')
    app.register_blueprint(message.message, url_prefix='/message')

    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create sql tables for our data models
        return app
