# extensions/login_manager.py
from flask_login import LoginManager
from app.models.user_model import User
login_manager = LoginManager()

def init_login_manager(app):
    """Initialize Flask-Login."""
    login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    """Load a user from the database by ID."""
    return User.query.get(int(user_id))
