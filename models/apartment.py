from models import db
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.schema import CheckConstraint


class Apartment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    property_id =  mapped_column(ForeignKey('property.id'), nullable=False)
    # Navigation property 
    property = relationship( 'Property', back_populates='apartments')
    apartment_number: Mapped[int] = mapped_column(nullable=False)
    apartment_type:Mapped[str]
    image:Mapped[str]
    floor:Mapped[int] = mapped_column(nullable=False)
    resident_id = mapped_column(ForeignKey('user.id'), nullable=True, unique= True)
    # Navigation Property 
    resident = relationship('User',back_populates='apartment')



