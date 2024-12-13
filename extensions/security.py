# extensions/security.py
from flask_security import Security, SQLAlchemySessionUserDatastore
from models.user_model import User, Role
from database import db

# Initialize the user data store and security
user_datastore = None
security = Security()

def init_security(app, db):
    """Initialize Flask-Security."""
    global user_datastore
    user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
    security.init_app(app, user_datastore)
