from models import db
from sqlalchemy import ForeignKey, String, Integer, Date
from sqlalchemy.orm  import Mapped, mapped_column, relationship

class Agreement(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement=True)
    resident_id = mapped_column(ForeignKey('user.id'),nullable=False)
    apartment_id =mapped_column(ForeignKey('apartment.id'), nullable=False)
    # Navigation Property 
    apartment = relationship('Apartment')
    resident = relationship('User', back_populates="agreements", uselist= False)
    lease_start_date : Mapped[str] = mapped_column(Date, nullable=False)
    monthly_rent: Mapped[int] = mapped_column(Integer, nullable= False)
    monthly_rental_due_date : Mapped[str] =  mapped_column(Integer, nullable=False)
    lease_end_date: Mapped[str] = mapped_column(Date,nullable=False)
    signed_lease_document = db.Column(db.String(200), nullable=True)