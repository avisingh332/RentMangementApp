from models import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Integer, Enum as SqlEnum, Date, DateTime
from sqlalchemy.orm  import Mapped, mapped_column, relationship
from models.enums import PaymentMethod

class Payment(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement= True)
    bill_id = mapped_column(ForeignKey('bill.id'), nullable= False)
    # payment_status= mapped_column(SqlEnum(PaymentStatus), nullable= False, default=PaymentStatus.DUE)
    amount_paid: Mapped[int] = mapped_column(nullable=False)
    paid_at: Mapped[str] = mapped_column(DateTime, nullable=True)
    payment_method = mapped_column(SqlEnum(PaymentMethod), nullable= False)
    # Navigation property 
    bill = relationship('Bill', back_populates='payments', uselist= False)