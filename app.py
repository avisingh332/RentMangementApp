from flask import Flask , render_template, request, redirect, url_for
from database.db import db, init_db
from models.item_model import Item
from extensions.security import init_security
from extensions.login_manger import init_login_manager
from flask_login import current_user, login_manager, login_required, login_user
from flask_security import roles_accepted
from werkzeug.security import check_password_hash
from data import maintenance_records, report_data, status_list
app = Flask(__name__, template_folder="templates")

app.config.update({
    'SQLALCHEMY_DATABASE_URI' : 'sqlite:///db.sqlite',
    'SQLALCHEMY_TRACK_MODIFICATIONS' : False,
    'SECURITY_PASSWORD_SALT':'MY_SECRET',
    'SECURITY_REGISTERABLE':True,
    'SECURITY_SEND_REGISTER_EMAIL':False,
    'SECRET_KEY': 'My_Very_Own_Secret_Key'
})

# binds the db object to flask app
db.init_app(app)
# method to create database tables
init_db(app)
init_security(app, db)
init_login_manager(app)

from models.user_model import User, Role

def role_check(role):
    if role in [role.name for role in current_user.roles]:
        return True
    else :
        return False 
    
app.jinja_env.globals['role_check'] = role_check

@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('signin'))
    
    if role_check('Resident'):
        print("Resident")

    if role_check('Resident'):
       return redirect(url_for('user_home'))

    else:
        return redirect(url_for('admin_home'))
    
from datetime import date


@app.route('/admin-home')
@login_required
@roles_accepted('Admin')
def admin_home():
   
    return render_template('./admin/admin_home.html', data=report_data)

@app.route('/user-home')
@login_required
@roles_accepted("Resident")
def user_home():
    return render_template('/user/user_home.html')

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
        return render_template('maintenance.html', records = maintenance_records, status_list = status_list)

@app.route('/maintenance/create', methods=['GET', 'POST'])
def create_maintenance():
    if request.method =='POST':
        pass
    else:
        return render_template('create_maintenance.html')

if(__name__ == "__main__"):
    app.run(debug=True);


