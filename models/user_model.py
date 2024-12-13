from database.db import db
from flask_login import UserMixin
from flask_security import RoleMixin
from sqlalchemy import String
from sqlalchemy.orm import validates, mapped_column, Mapped, relationship

# Create a table in the database for storing roles
class Role(db.Model, RoleMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

# Create a table in the database for assigning roles
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer,  db.ForeignKey('user.id', ondelete='CASCADE')),
    db.Column('role_id', db.Integer,  db.ForeignKey('role.id', ondelete='CASCADE'))
)


# Create a table in the database for storing users
class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False, server_default='')
    active: Mapped[bool] = mapped_column()
    roles: Mapped[list[Role]] = relationship(Role, secondary='roles_users', backref=db.backref('users', lazy='dynamic'))
    fs_uniquifier: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)


