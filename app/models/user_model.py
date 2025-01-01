from app.models import db
from flask_login import UserMixin
from flask_security import RoleMixin
from sqlalchemy import String, Boolean
from sqlalchemy.orm import validates, mapped_column, Mapped, relationship

# Create a table in the database for storing roles
class Role(RoleMixin,db.Model ):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

# Create a table in the database for assigning roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer,  db.ForeignKey('user.id', ondelete='CASCADE'), nullable= False),
    db.Column('role_id', db.Integer,  db.ForeignKey('role.id', ondelete='CASCADE'),  nullable= False)
)
# Create a table in the database for storing users
class User(UserMixin, db.Model ):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    name:Mapped[str] = mapped_column(String(15),nullable=False)
    username:Mapped[str] = mapped_column(nullable=True)
    password: Mapped[str] = mapped_column(nullable=True)
    active: Mapped[bool] = mapped_column(default=False)
    roles: Mapped[list[Role]] = relationship(Role, secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    is_registered: Mapped[bool] = mapped_column( Boolean, nullable=False, default= False)
    fs_uniquifier: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    # navigation property
    apartment = relationship('Apartment', uselist=False, back_populates="resident")
    maintenances = relationship('Maintenance',uselist=True, back_populates='resident')
    agreements = relationship('Agreement', uselist= True, back_populates='resident')


