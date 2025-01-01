from flask import Flask
from .models import db, init_db
from .extensions.login_manger import init_login_manager
from .extensions.security import init_security
from .utils import role_check
from .models import db, init_db
from app.blueprints.user import user_bp
from app.blueprints.main import main_bp
from app.blueprints.admin import admin_bp
from app.utils import start_scheduler

import os


# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE_DIR = os.path.join(BASE_DIR, 'database')
# os.makedirs(DATABASE_DIR, exist_ok=True)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # This gets the current file's directory
DATABASE_DIR = os.path.join(BASE_DIR, '..', 'database')  # This points to the 'database' folder outside the 'app' directory
os.makedirs(DATABASE_DIR, exist_ok=True)

configuration_dict ={
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{os.path.join(DATABASE_DIR, "db.sqlite")}',
    'SQLALCHEMY_TRACK_MODIFICATIONS' : False,
    'SECURITY_PASSWORD_SALT':'MY_SECRET',
    'SECURITY_REGISTERABLE':False,
    'SECURITY_SEND_REGISTER_EMAIL':False,
    'SECRET_KEY': 'My_Very_Own_Secret_Key',
    'SCHEDULER_API_ENABLED': True, 
    'UPLOAD_FOLDER':'static/uploads'
}

def create_app(configuration_dict =configuration_dict):
    app = Flask(__name__, template_folder='app/templates')

    app.config.update(configuration_dict)

    db.init_app(app)
    init_db(app)
    init_security(app, db)
    init_login_manager(app)

    app.jinja_env.globals['role_check'] = role_check
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(main_bp)
    
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler(app)
    return app
    