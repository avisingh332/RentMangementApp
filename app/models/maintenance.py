from app.models import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, String, Integer, Enum as SqlEnum
from sqlalchemy.orm  import Mapped, mapped_column, relationship
from app.models.enums import CategoryEnum, PriorityEnum, StatusEnum

def get_enum_values(enum_class):
    return [member.value for member in enum_class]

class Maintenance(db.Model):
    id : Mapped[int] = mapped_column(Integer, primary_key= True, autoincrement= True)
    resident_id = mapped_column(ForeignKey('user.id'),nullable= False)
    # navigation prop
    resident = relationship('User', uselist=False, back_populates='maintenances')
    description: Mapped[str] = mapped_column(String(100), nullable=False)
    category= mapped_column(SqlEnum(CategoryEnum), nullable=False)
    priority= mapped_column(SqlEnum(PriorityEnum), nullable=False)
    status = mapped_column(SqlEnum(StatusEnum))
    comment:Mapped[str] = mapped_column(String(50), nullable=True)
