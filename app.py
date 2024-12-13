from flask import Flask , render_template, request, redirect, url_for
from database.db import db, init_db
from models.item_model import Item
from extensions.security import init_security
from extensions.login_manger import init_login_manager
from flask_login import login_manager, login_user
from flask_security import roles_accepted
from werkzeug.security import check_password_hash

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

@app.route('/')
def home():
    return render_template('home.html')


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
                # return redirect(url_for('home'))
                return "Used Logged in Successfully!!!"
            # if password doesn't match
            else:
                msg="Wrong password"
        
        # if user does not exist
        else:
            msg="User doesn't exist"
        return render_template('signin.html', msg=msg)
        
    else:
        return render_template("signin.html", msg=msg)


@app.route('/residents', methods=['GET'])
# @roles_accepted( ['Admin'] )
def residents():
    return "Hello world"


if(__name__ == "__main__"):
    app.run(debug=True);