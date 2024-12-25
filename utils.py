from flask import current_app
from models import db
from models.agreement import Agreement
from  models.payment import  Payment
from datetime import date
from flask_apscheduler import APScheduler
from models.bill import Bill

scheduler = APScheduler()

@scheduler.task(id ="Job-1", 
    trigger ='cron', 
    day=25, 
    hour =15,
    minute=22,
    second = 15, 
    misfire_grace_time=900, 
    coalesce=True, 
    max_instances=1
    )
def generate_monthly_bill():
    """Generates payment records for all active agreements on the first day of the month."""
    with scheduler.app.app_context():
        today = date.today()
        # if today.day != 1:  
        #     print("Wrong Date...")
        #     return  # Ensure this method only runs on the 1st of the month
        
        active_agreements = db.session.query(Agreement).filter(
            Agreement.lease_start_date <= today,
            Agreement.lease_end_date >= today
        ).all()

        print("Active Agreements: \n")
        for agreement in active_agreements:
            # print(f"{agreement.id}-> {agreement.resident.name}")
            # Check if a payment record already exists for this month
            existing_bill = db.session.query(Bill).filter(
                Bill.agreement_id == agreement.id,                
                Bill.month == today.replace(day=1)
            ).first()
            if existing_bill is None:
                # Create a new payment record
                bill = Bill(
                    agreement_id=agreement.id,
                    bill_amount=agreement.monthly_rent,
                    month = today.replace(day=1)
                )
                db.session.add(bill)
        
        db.session.commit()



def start_scheduler(app):
    """Start the scheduler to generate payments on the 1st of every month."""
    scheduler.init_app(app)
    scheduler.start()
