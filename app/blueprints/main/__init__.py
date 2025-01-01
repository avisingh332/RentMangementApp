from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required
from flask_security import roles_accepted
from app.models import db
from app.models.maintenance import Maintenance
from app.models.user_model import User
from app.models.enums import StatusEnum, PriorityEnum, CategoryEnum
from app.utils import role_check
from werkzeug.security import check_password_hash , generate_password_hash
from flask_login import current_user, login_required, login_user
import re

main_bp = Blueprint('main_bp', __name__, template_folder='templates')


@main_bp.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('main_bp.signin'))

    if role_check('Resident'):
        return redirect(url_for('user_bp.user_home'))

    else:
        return redirect(url_for('admin_bp.admin_home'))
    

# signin page
@main_bp.route('/signin', methods=['GET', 'POST'])
def signin():
    msg=""
    
    if request.method == 'POST':
        # search user in database
        username = request.form['username']
        password = request.form['password']
        if(username =='' or password ==''):
            flash("Please enter your username and pasword", 'warning')
            return redirect(url_for('main_bp.signin'))
        
        # search user in database using username and password
        user = db.session.query(User).filter(User.username == username).first()
        # if exist check password
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            flash("Logged In Successfully", "success")
            return redirect(url_for('main_bp.home'))
            # if password doesn't match
        else:
            flash("Email or Password Incorrect!!!", 'danger')
            return redirect(url_for('main_bp.signin'))
        
    else:
        if current_user.is_authenticated:
            flash("User Already Logged in ", 'warning')
            return redirect(url_for('main_bp.home'))
        else:
            return render_template("signin.html", msg=msg)

@main_bp.route('/register', methods = ['POST','GET'])
def register():
    # Define the regex pattern for the username
    USERNAME_REGEX = r"^(?!_)[a-zA-Z0-9_]{3,20}(?<!_)$"

    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password'].strip()
        confirm_password = request.form['confirm_password'].strip()
        user = User.query.filter_by(email = email).first()
        if user:
            if user.is_registered:
                flash(f"User Already Registered with Username: {user.username}  Login Please",'warning')
                return redirect(url_for('main_bp.signin'))
            # write regex to check username

            elif password!= confirm_password or re.match(USERNAME_REGEX, username) is None:
                flash("Invalid User name or Password", 'danger')
                return redirect(url_for('main_bp.register'))
            else:
                user.username = username
                user.password = generate_password_hash(password) 
                db.session.commit()
                flash(f"User Registered Successfully with Username: {user.username}  Login Now",'success')
                return redirect(url_for('main_bp.signin'))
        else:
            flash("You are not authorized to register as a user", 'danger')
            return render_template('register.html')        
    else:
        return render_template('register.html')
    
@main_bp.route('/maintenance', methods=['GET'])
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
