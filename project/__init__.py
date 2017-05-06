from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    bootstrap.init_app(app)
    db.init_app(app)

    uri = config[config_name].SQLALCHEMY_DATABASE_URI

    from database import init_db
    init_db(uri)

    login_manager.init_app(app)
    login_manager.login_view = '/login'

    from project.users.views import user_blueprint
    app.register_blueprint(user_blueprint)

    from project.home.views import home_blueprint
    app.register_blueprint(home_blueprint, url_prefix='/home')

    from project.models.user import User

    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()

    return app

