from flask import Flask , render_template, request, redirect, url_for, flash
from models import db, init_db
from models.user_model import User, Role, roles_users
from models.maintenance import Maintenance
from models.enums import CategoryEnum, PriorityEnum, StatusEnum, PaymentMethod
from extensions.security import init_security
from extensions.login_manger import init_login_manager
from flask_login import current_user, login_required, login_user
from flask_security import roles_accepted
from werkzeug.security import check_password_hash
from utils import start_scheduler
from blueprints.user import user_bp
from blueprints.admin import admin_bp
import os



app = Flask(__name__, template_folder="templates")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DATABASE_DIR, exist_ok=True)

app.config.update({
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{os.path.join(DATABASE_DIR, "db.sqlite")}',
    'SQLALCHEMY_TRACK_MODIFICATIONS' : False,
    'SECURITY_PASSWORD_SALT':'MY_SECRET',
    'SECURITY_REGISTERABLE':True,
    'SECURITY_SEND_REGISTER_EMAIL':False,
    'SECRET_KEY': 'My_Very_Own_Secret_Key',
    'SCHEDULER_API_ENABLED': True, 
    'UPLOAD_FOLDER':'static/uploads'
})

# binds the db object to flask app
db.init_app(app)

# method to create database tables
init_db(app)
init_security(app, db)
init_login_manager(app)


def role_check(role):
    if role in [role.name for role in current_user.roles]:
        return True
    else :
        return False 
    
app.jinja_env.globals['role_check'] = role_check


app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(admin_bp, url_prefix='/admin')


@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('signin'))

    if role_check('Resident'):
        return redirect(url_for('user_bp.user_home'))

    else:
        return redirect(url_for('admin_bp.admin_home'))
    



# signin page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg=""
    if request.method == 'POST':
        # search user in database
        user = User.query.filter_by(email=request.form['email']).first()
        # if exist check password
        if user:
            if check_password_hash(user.password, request.form['password']):
                # if password matches, login the user
                login_user(user)
                
            # if password doesn't match
            else:
                msg="Wrong password"
        
        return redirect(url_for('home'))
        
    else:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        else:
            return render_template("signin.html", msg=msg)

@app.route('/maintenance', methods=['GET'])
@login_required
def maintenance():
    if request.method =='POST':
        pass
    else:
        maintenance = None
        if role_check('Admin'):
            maintenances = db.session.query(Maintenance).all()
        else:
            maintenances = db.session.query(Maintenance).filter(Maintenance.resident_id == current_user.get_id())

        return render_template(
            'maintenance.html',
            records = maintenances,
            StatusEnum = StatusEnum,
            PriorityEnum = PriorityEnum,
            CategoryEnum = CategoryEnum
            )


if(__name__ == "__main__"):
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler(app)
    app.run(debug=True);


