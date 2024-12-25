from models import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Integer, Enum as SqlEnum, Date, DateTime
from sqlalchemy.orm  import Mapped, mapped_column, relationship

class Bill(db.Model):
    id:Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement= True)
    agreement_id = mapped_column(ForeignKey('agreement.id'), nullable= False)
    # payment_status= mapped_column(SqlEnum(PaymentStatus), nullable= False, default=PaymentStatus.DUE)
    bill_amount: Mapped[int] = mapped_column(nullable=False)
    month : Mapped[str]  = mapped_column(Date, nullable=False)
    amount_paid: Mapped[str] = mapped_column(Integer, nullable=True)
    # Navigation property 
    agreement = relationship('Agreement', uselist= False)
    payments = relationship('Payment', uselist=True)