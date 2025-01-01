from flask import url_for
from flask_login import current_user
from app.models.user_model import User
from app.models import db


def test_resident_signin_success(client, app):
    with app.test_request_context():
        response = client.post(
            url_for('main_bp.signin'),
            data={'email': 'user1@example.com', 'password': 'user123'},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert current_user.is_authenticated
        assert current_user.email == 'user1@example.com'
        assert current_user.roles[0].name == 'Resident'

# write admin signing success

def test_admin_signin_success(client, app):
    with app.test_request_context():
        response = client.post(
            url_for('main_bp.signin'),
            data={'email': 'admin@example.com', 'password': 'admin123'},
            follow_redirects=True
        )
        # write assertions
        assert response.status_code == 200
        assert current_user.is_authenticated
        assert current_user.email == 'admin@example.com'
        assert current_user.roles[0].name == 'Admin'

def test_logout_success(client, app):
    with app.test_request_context():
        response = client.post(
            url_for('main_bp.signin'),
            data={'email': 'user1@example.com', 'password': 'user123'},
            follow_redirects=True
        )
        assert response.status_code == 200
        assert current_user.is_authenticated
        
        response = client.post(
            '/logout',
            follow_redirects=True
        )
        assert response.status_code == 200
        assert not current_user.is_authenticated

def test_admin_home_success(client, app):
    # first do a login using test_signin_success method declared above
    
    # then simulate admin accessing admin_home route
    test_admin_signin_success(client, app)

    with app.test_request_context():
        response = client.get(
            url_for('admin_bp.admin_home'),
            follow_redirects=True
        )
        assert response.status_code == 200
        assert current_user.is_authenticated
        assert current_user.roles[0].name == 'Admin'
        # assert some data in the response
        # complete below line
        # assert b"<h4>Monthly Rental Table</h4>" in 

def test_admin_home_failure(client,app):
    # simulate user accessing admin_home route
    test_resident_signin_success(client, app)
    
    with app.test_request_context():
        response = client.get(
            url_for('admin_bp.admin_home'),
            follow_redirects=True
        )
        print(response.status_code)
        assert response.status_code == 403
        