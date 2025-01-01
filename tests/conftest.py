import pytest
from flask import url_for
from app.models.user_model import User
from flask_login import current_user
import uuid
from app import create_app
from app.models import db
from app.extensions import login_manger, security

@pytest.fixture()
def app():
    configuration_dict ={
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'SQLALCHEMY_TRACK_MODIFICATIONS' : False,
        'SECURITY_PASSWORD_SALT':'MY_SECRET',
        'SECURITY_REGISTERABLE':False,
        'SECURITY_SEND_REGISTER_EMAIL':False,
        'SECRET_KEY': 'My_Very_Own_Secret_Key',
        'SCHEDULER_API_ENABLED': True, 
        'UPLOAD_FOLDER':'static/uploads',
        "TESTING": True,
        "SERVER_NAME": "localhost"
    }
    app = create_app(configuration_dict)
    # app.config.update(configuration_dict)
    # with app.app_context():
    #     db.create_all()
    yield app
    
    # Clean-up steps
    with app.app_context():
        db.session.remove()
        db.drop_all()
    
@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def seed_user_data(app): 
    with app.app_context():
        user = User(
            email="test@example.com",  # Changed to match the email in the test
            password="testpassword",   # Changed to match the password in the test
            name="test_user",
            active=True,
            fs_uniquifier=str(uuid.uuid4())
        )
        db.session.add(user)
        db.session.commit()
    
    yield

    # Clean up
    with app.app_context():
        User.query.filter_by(email="test@example.com").delete()
        db.session.commit()
    