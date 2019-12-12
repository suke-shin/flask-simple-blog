import os
from base64 import b64encode
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_dropzone import Dropzone

db = SQLAlchemy()

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(__name__)
    dropzone = Dropzone(app)

    app.config['SECRET_KEY'] = 'mysecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['UPLOADED_PATH'] = os.path.join(basedir, 'static/images')
    app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image'
    app.config['DROPZONE_MAX_FILE_SIZE'] = 3
    app.config['DROPZONE_MAX_FILES'] = 1
    app.config['DROPZONE_IN_FORM'] = True
    app.config['DROPZONE_UPLOAD_ON_CLICK'] = True
    app.config['DROPZONE_UPLOAD_ACTION'] = 'main.handle_upload'
    app.config['DROPZONE_UPLOAD_BTN_ID'] = 'submit'

    db = SQLAlchemy(app)

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app