from enum import Enum

class CategoryEnum(Enum):
    PLUMBING = "Plumbing"
    ELECTRICAL = "Electrical"
    HARDWARE = "Hardware"
    APPLIANCES = "Appliances"

class PriorityEnum(Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class StatusEnum(Enum):
    IN_PROGRESS = "InProgress"
    PENDING = "Pending"
    COMPLETE = "Complete"

class PaymentStatus(Enum):
    DUE= "Due"
    PAID = "Paid"

class PaymentMethod(Enum):
    CARD = "Card"
    UPI = "UPI"
    NET_BANKING = "Net Banking"