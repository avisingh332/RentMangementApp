from models.user_model import User, Role
from werkzeug.security import generate_password_hash
import uuid
# Seed roles
def seed_roles(db):
    """Seed the database with roles."""
    if Role.query.first():
        print("Roles already exist. Skipping role seeding.")
        return
    
    # Create roles (including Resident as default)
    roles = [
        Role(name="Admin"),
        Role(name="Resident")  # Default role to be assigned to users
    ]
    
    # Add roles to the session and commit
    db.session.add_all(roles)
    db.session.commit()
    print("Roles seeded successfully.")

# Seed users and assign the "Resident" role to each
def seed_users_assign_roles(db):
    """Seed the database with users and hashed passwords."""
    if User.query.first():
        print("Users already exist. Skipping user seeding.")
        return
    
    # Define sample users with plaintext passwords
    sample_users = [
        {"email": "admin@example.com", "password": "admin123", "active": True, "roles": ["Admin"]},
        {"email": "user1@example.com", "password": "user123", "active": True, "roles": ["Resident"]},
        {"email": "user2@example.com", "password": "user123", "active": True, "roles": ["Resident"]},
        {"email": "user3@example.com", "password": "user123", "active": True, "roles": ["Resident"]},
    ]
    
    # Create users and assign roles
    for user_data in sample_users:
        hashed_password = generate_password_hash(user_data["password"])
        user = User(email=user_data["email"], password=hashed_password, active=user_data["active"], fs_uniquifier=str(uuid.uuid4()) )
        # Assign roles to users
        for role_name in user_data["roles"]:
            role = Role.query.filter_by(name=role_name).first()
            if role:
                user.roles.append(role)
        db.session.add(user)
    # Commit the changes
    db.session.commit()
    print("Users and roles assigned successfully.")

def seed(db):
    seed_roles(db)
    seed_users_assign_roles(db)
