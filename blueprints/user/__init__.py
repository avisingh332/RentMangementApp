from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required
from flask_security import roles_accepted
from models import db
from models.agreement import Agreement
from models.property import Property
from models.apartment import Apartment
from models.maintenance import Maintenance
from models.user_model import User
from models.bill import Bill
from models.enums import PaymentMethod, StatusEnum, CategoryEnum,PriorityEnum
from models.payment import Payment
from datetime import datetime

user_bp = Blueprint('user_bp', __name__, template_folder='templates')

@user_bp.route('/home')
@login_required
@roles_accepted("Resident")
def user_home():
    user_agreement = db.session.query(Agreement).filter(Agreement.resident_id == current_user.get_id()).first()
    property_details = db.session.query(Apartment, Property).join(Property).filter(Apartment.resident_id == user_agreement.resident_id).first()
    bills = db.session.query(Bill).join(Agreement).join(User).filter(User.id == current_user.get_id())

    processed_bill_data = []
    for rec in bills:
        payment_status = ""
        if rec.amount_paid is None or rec.amount_paid ==0:
            payment_status = "Not Paid"
        elif rec.bill_amount == rec.amount_paid:
            payment_status="Full Payment"
        else:
            payment_status= "Partial Payment"

        due_amount = rec.bill_amount
        if rec.amount_paid is not None  and rec.amount_paid != 0:
            due_amount = rec.bill_amount - rec.amount_paid
        processed_record = {
            "bill_id": rec.id,
            "bill_amount":rec.bill_amount,
            "amount_paid":0 if rec.amount_paid is None else rec.amount_paid ,
            "payment_status":payment_status,
            "amount_due": due_amount,
            "month": rec.month
        }
        processed_bill_data.append(processed_record)
    print(processed_bill_data)
    if property_details:
        apartment, property = property_details
    else:
        apartment, property = None, None

    return render_template(
        'user_home.html',
        apartment=apartment,
        property=property, 
        user_agreement = user_agreement,
        bills = processed_bill_data
    )

@user_bp.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method =='GET':
        bill_id = request.args.get('bill_id')
        bill = db.session.query(Bill).filter(Bill.id == bill_id).first()
        amount = bill.bill_amount
        if bill.amount_paid is not None:
            amount  = amount - bill.amount_paid
        print(f"Got Bill id as : {bill_id}")
        return render_template('payment.html',
                            bill_id=bill_id,
                            amount=amount,
                            PaymentMethod = PaymentMethod)

    else:
        bill_id = request.form['bill_id']
        amount = float(request.form['amount'])
        payment_method = request.form['payment_method']
        print(f'{bill_id}-> {amount}-> {payment_method}')
        # Process the payment logic (e.g., update the database)
        bill = db.session.query(Bill).filter(Bill.id == bill_id).first()
        if bill:
            new_payment = Payment(bill_id =bill_id,
                                amount_paid =amount,
                                paid_at = datetime.now(),
                                payment_method = PaymentMethod(payment_method) )
            db.session.add(new_payment)
            bill.amount_paid =0
            bill.amount_paid += amount
            db.session.commit()
            flash('Payment successful!', 'success')
        else:
            flash('Bill Not Found!', 'error')
        return redirect(url_for('user_bp.user_home'))  # Redirect back to the dashboard


@user_bp.route('/maintenance/create', methods=['GET', 'POST'])
@login_required
def create_maintenance():
    if request.method == 'POST':
        # Fetch data from the form
        category = request.form.get('category')
        priority = request.form.get('priority')
        description = request.form.get('description')
        # print(f"{category}, {priority}, {description}");
        # return redirect(url_for('maintenance'))
        # Simulate logged-in user (use actual user in real implementation)
        logged_in_user_id = current_user.get_id()  # Replace with actual logged-in user ID from session

        # Validate data (if needed)
        if not category or not priority or not description:
            flash("All fields are required!", "danger")
            return redirect(url_for('create_maintenance'))

        # Create new maintenance request
        new_maintenance = Maintenance(
            resident_id=logged_in_user_id,
            category=CategoryEnum(category),
            priority=PriorityEnum(priority),
            description=description,
            status=StatusEnum.PENDING  # Default status for a new request
        )
        # for attr, value in new_maintenance.__dict__.items():
        #     if not attr.startswith('_'):  # Skip internal attributes
        #         print(f"Property: {attr}, Value: {value}")
        
        db.session.add(new_maintenance)
        db.session.commit()

        flash("Maintenance request created successfully!", "success")
        return redirect(url_for('maintenance'))  # Redirect to the main maintenance page
    else:
        # Render the form template for GET request
        return render_template(
            'create_maintenance.html',
            CategoryEnum = CategoryEnum,
            PriorityEnum = PriorityEnum)
