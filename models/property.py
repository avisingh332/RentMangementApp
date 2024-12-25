from models import db
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship

class Property(db.Model):
    id:Mapped[int] = mapped_column(primary_key= True, autoincrement=True)
    registration_number :Mapped[int] = mapped_column(nullable=False)
    name:Mapped[str] = mapped_column(String(30), nullable=False)
    address:Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    phone_number =mapped_column(String(10) ,nullable= False)
    apartments = relationship('Apartment', back_populates='property')