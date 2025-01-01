from app.models.user_model import User, Role
from app.models.apartment import Apartment
from app.models.property import Property
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from app.models.agreement import Agreement
from app.models.maintenance import Maintenance
import uuid
from app.models.enums import CategoryEnum, PriorityEnum, StatusEnum


# Seed roles
def seed_roles(db:SQLAlchemy):
    """Seed the database with roles."""
    if db.session().query(Role).count():
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
def seed_users_assign_roles(db:SQLAlchemy):
    """Seed the database with users and hashed passwords."""
    if db.session.query(User).count():
        print("Users already exist. Skipping user seeding.")
        return
    
    # Define sample users with plaintext passwords
    sample_users = [
        {"email": "admin@example.com", "name":"Admin-User",  "active": True, "roles": ["Admin"]},
        {"email": "user1@example.com", "name":"User 1",   "active": True, "roles": ["Resident"]},
        {"email": "user2@example.com", "name":"User 2",  "active": True, "roles": ["Resident"]},
        {"email": "user3@example.com", "name":"User 3",  "active": True, "roles": ["Resident"]},
    ]
    
    user_list = []
    # Create users and assign roles
    for user_data in sample_users:
        # hashed_password = generate_password_hash(user_data["password"])
        user = User(email=user_data["email"], name= user_data["name"], active= False, fs_uniquifier=str(uuid.uuid4()) )
        # Assign roles to users
        for role_name in user_data["roles"]:
            role = Role.query.filter_by(name=role_name).first()
            if role:
                user.roles.append(role)
        # db.session.add(user)
        user_list.append(user)
    # Commit the changes
    # user_list[1].active = True
    # user_list[0].active = True
    # user_list[0].is_registered = True
    # user_list[1].is_registered = True
    # user_list[0].password = generate_password_hash('admin123')
    # user_list[1].password = generate_password_hash('user123')
    db.session.add_all(user_list)
    db.session.commit()
    print("Users and roles assigned successfully.")

def seed_properties(db:SQLAlchemy):
    """Seed dummy properties if none exist in the database."""
    if not db.session.query(Property).count():
        # Create dummy properties
        properties = [
            Property(
                registration_number=1001,
                name="Greenwood Estate",
                address="123 Main Street, Downtown",
                description="Luxury apartments with modern amenities.",
                phone_number="1234567890"
            ),
            Property(
                registration_number=1002,
                name="Sunset Apartments",
                address="456 Oak Avenue, Suburbia",
                description="Affordable living with great views.",
                phone_number="0987654321"
            ),
            Property(
                registration_number=1003,
                name="Pine View Heights",
                address="789 Pine Road, Uptown",
                description="Spacious apartments in a serene environment.",
                phone_number="1112223333"
            ),
        ]
        db.session.add_all(properties)
        db.session.commit()
        print("Seeded properties successfully.")

def seed_apartments(db: SQLAlchemy):
    """Seed dummy apartments if none exist in the database."""
    if not db.session.query(Apartment).count():
        # Fetch existing properties for relationships
        properties = db.session.query(Property).all()

        if not properties:
            print("No properties found. Seed properties first.")
            return

        # Fetch users with 'Resident' role
        residents = db.session.query(User).join(User.roles).filter(Role.name == 'Resident').all()

        if not residents:
            print("No residents found. Seed users first.")
            return

        # Create dummy apartments and assign a resident to each apartment
        apartments = [
            Apartment(
                property_id=properties[0].id,
                apartment_number=101,
                apartment_type="2BHK",
                image="image1.jpg",
                floor=1,
                resident_id=residents[0].id  # Assigning the first resident to this apartment
            ),
            Apartment(
                property_id=properties[0].id,
                apartment_number=102,
                apartment_type="3BHK",
                image="image2.jpg",
                floor=1,
                resident_id=residents[1].id  # Assigning the second resident to this apartment
            ),
            Apartment(
                property_id=properties[1].id,
                apartment_number=201,
                apartment_type="1BHK",
                image="image3.jpg",
                floor=2,
                resident_id=residents[2].id  # Assigning the third resident to this apartment
            ),
            Apartment(
                property_id=properties[1].id,
                apartment_number=202,
                apartment_type="Studio",
                image="image4.jpg",
                floor=2
            ),
            Apartment(
                property_id=properties[2].id,
                apartment_number=301,
                apartment_type="4BHK",
                image="image5.jpg",
                floor=3
            ),
        ]

        db.session.add_all(apartments)
        db.session.commit()
        print("Seeded apartments successfully.")

def seed_agreements(db: SQLAlchemy):
    """Seed rental agreements for apartments if none exist."""
    if not db.session.query(Agreement).count():
        # Fetch existing apartments with residents
        apartments = db.session.query(Apartment).filter(Apartment.resident_id.isnot(None)).all()

        if not apartments:
            print("No apartments with residents found. Ensure apartments and residents are seeded.")
            return

        agreements = []

        # Create a dummy agreement for each apartment with a resident
        for apartment in apartments:
            lease_start_date = (datetime.now()- timedelta(days=30)).date()
            agreements.append(
                Agreement(
                    apartment_id=apartment.id,
                    resident_id=apartment.resident_id,  # Use the existing resident ID
                    lease_start_date=(datetime.now()- timedelta(days=30)).date(),  # Today's date as lease start
                    lease_end_date=(datetime.now() + timedelta(days=365)).date(),  # 1-year lease
                    monthly_rent=15000 + (apartment.floor * 500),  # Example rent calculation
                    monthly_rental_due_date= lease_start_date.day ,  # Rent due in 30 days
                )
            )

        # Add and commit the agreements to the database
        db.session.add_all(agreements)
        db.session.commit()
        print("Seeded agreements successfully.")
    else:
        print("Agreements already exist. Skipping seeding.")

def seed_maintenance(db: SQLAlchemy):
    """Seed maintenance records for residents."""
    if not db.session.query(Maintenance).count():
        # Fetch residents
        residents = db.session.query(User).join(User.roles).filter(Role.name == 'Resident').all()

        if not residents:
            print("No residents found. Ensure users and roles are seeded.")
            return

        maintenance_records = []

        # Create dummy maintenance records for each resident
        for resident in residents:
            maintenance_records.append(
                Maintenance(
                    resident_id=resident.id,
                    description="Fixing plumbing issues in the apartment.",
                    category=CategoryEnum.PLUMBING.name,
                    priority=PriorityEnum.HIGH.name,
                    status=StatusEnum.PENDING.name
                )
            )
            maintenance_records.append(
                Maintenance(
                    resident_id=resident.id,
                    description="Electrical system maintenance and repairs.",
                    category=CategoryEnum.ELECTRICAL.name,
                    priority=PriorityEnum.MEDIUM.name,
                    status=StatusEnum.IN_PROGRESS.name
                )
            )
            maintenance_records.append(
                Maintenance(
                    resident_id=resident.id,
                    description="Appliance repair for malfunctioning refrigerator.",
                    category=CategoryEnum.APPLIANCES.name,
                    priority=PriorityEnum.LOW.name,
                    status=StatusEnum.COMPLETE.name
                )
            )


        # Add and commit the maintenance records to the database
        db.session.add_all(maintenance_records)
        db.session.commit()
        print("Seeded maintenance records successfully.")
    else:
        print("Maintenance records already exist. Skipping seeding.")


def seed(db):
    seed_roles(db)
    seed_users_assign_roles(db)
    seed_properties(db)
    seed_apartments(db)
    seed_agreements(db)
    seed_maintenance(db)
