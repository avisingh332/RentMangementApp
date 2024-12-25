from flask import Flask , render_template, request, redirect, url_for, flash
from models import db, init_db
from models.apartment import  Apartment
from models.property import Property
from models.user_model import User, Role, roles_users
from models.maintenance import Maintenance
from models.bill import Bill
from models.agreement import Agreement
from models.payment import Payment
from models.enums import CategoryEnum, PriorityEnum, StatusEnum, PaymentMethod
from extensions.security import init_security
from extensions.login_manger import init_login_manager
from flask_login import current_user, login_manager, login_required, login_user
from flask_security import roles_accepted
from werkzeug.security import check_password_hash
from sqlalchemy import case, func
from utils import start_scheduler
from datetime import date, datetime

import os
app = Flask(__name__, template_folder="templates")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, 'database')
os.makedirs(DATABASE_DIR, exist_ok=True)

app.config.update({
    'SQLALCHEMY_DATABASE_URI': f'sqlite:///{os.path.join(DATABASE_DIR, "db.sqlite")}',
    'SQLALCHEMY_TRACK_MODIFICATIONS' : False,
    'SECURITY_PASSWORD_SALT':'MY_SECRET',
    'SECURITY_REGISTERABLE':True,
    'SECURITY_SEND_REGISTER_EMAIL':False,
    'SECRET_KEY': 'My_Very_Own_Secret_Key',
    'SCHEDULER_API_ENABLED': True, 
    'UPLOAD_FOLDER':'static/uploads'
})

# binds the db object to flask app
db.init_app(app)

# method to create database tables
init_db(app)
init_security(app, db)
init_login_manager(app)


def role_check(role):
    if role in [role.name for role in current_user.roles]:
        return True
    else :
        return False 
    
app.jinja_env.globals['role_check'] = role_check

@app.route('/')
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('signin'))
    
    if role_check('Resident'):
        print("Resident")

    if role_check('Resident'):
       return redirect(url_for('user_home'))

    else:
        return redirect(url_for('admin_home'))
    

@app.route('/admin-home')
@login_required
@roles_accepted('Admin')
def admin_home():
    managed_properties_count = db.session.query(Property).count()
    apartment_units_count = db.session.query(Apartment).count()
    tenants_count = db.session.query(Agreement).count()
    active_maintenance_count = db.session.query(Maintenance).filter(Maintenance.status == StatusEnum.COMPLETE).count()
    
    data = db.session.query(
        User.name.label('tenant_name'),
        Agreement.monthly_rental_due_date.label('due_date'),
        Agreement.monthly_rent.label('monthly_rental'),
        Bill.month.label('month'),
        Bill.bill_amount.label('bill_amount'),
        Bill.amount_paid.label('amount_paid')
    ).join(Agreement,onclause=Bill.agreement_id == Agreement.id).join(User, onclause= Agreement.resident_id == User.id)
    
    processed_data = []
    for rec in data:
        status = ""
        
        if rec.amount_paid is None or rec.amount_paid == 0:
            if date.today().replace(day= rec.due_date) < date.today():
                status = "Overdue"
            else:
                status = "Not Paid"
        elif rec.amount_paid < rec.bill_amount:
            status = "Partially Paid"
        else:
            status = "Paid"
        due_amount =0
        if rec.amount_paid is None or rec.amount_paid==0:
            due_amount = rec.bill_amount
        else:
            due_amount = rec.bill_amount - rec.amount_paid
        processed_record = {
            "tenant_name": rec.tenant_name,
            "monthly_rental": rec.monthly_rental,
            "status": status,
            "bill_amount": rec.bill_amount,
            "due_amount": due_amount,
            "due_date": date.today().replace(day=rec.due_date, month= rec.month.month),
            "month": rec.month
        }
        processed_data.append(processed_record)


    return render_template(
        './admin/admin_home.html', data=processed_data,   
        managed_properties_count= managed_properties_count,
        apartment_units_count=  apartment_units_count,
        tenants_count= tenants_count,
        active_maintenance_count=active_maintenance_count)

@app.route('/user-home')
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
        '/user/user_home.html',
        apartment=apartment,
        property=property, 
        user_agreement = user_agreement,
        bills = processed_bill_data
    )

# signin page
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    msg=""
    if request.method == 'POST':
        # search user in database
        user = User.query.filter_by(email=request.form['email']).first()
        # if exist check password
        if user:
            if check_password_hash(user.password, request.form['password']):
                # if password matches, login the user
                login_user(user)
                
            # if password doesn't match
            else:
                msg="Wrong password"
        
        return redirect(url_for('home'))
        
    else:
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        else:
            return render_template("signin.html", msg=msg)

@app.route('/maintenance', methods=['GET'])
@login_required
def maintenance():
    if request.method =='POST':
        pass
    else:
        maintenance = None
        if role_check('Admin'):
            maintenances = db.session.query(Maintenance).all()
        else:
            maintenances = db.session.query(Maintenance).filter(Maintenance.resident_id == current_user.get_id())

        return render_template(
            'maintenance.html',
            records = maintenances,
            StatusEnum = StatusEnum,
            PriorityEnum = PriorityEnum,
            CategoryEnum = CategoryEnum
            )

@app.route('/maintenance/create', methods=['GET', 'POST'])
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


@app.route('/maintenance/update/<int:id>', methods=['POST'])
@login_required
def update_status(id):
    maintenance = db.session.get(Maintenance,id)
    if maintenance:
        # Update the status and the comment
        status = request.form['status']
        comment = request.form['comment']

        maintenance.status= StatusEnum(status)
        maintenance.comment = comment
        # maintenance.comment = request.form['comment']
        db.session.commit()
        flash('Status updated successfully', 'success')
    else:
        flash('Maintenance request not found', 'danger')

    return redirect(url_for('maintenance'))


@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    if request.method =='GET':
        bill_id = request.args.get('bill_id')
        bill = db.session.query(Bill).filter(Bill.id == bill_id).first()
        amount = bill.bill_amount
        if bill.amount_paid is not None:
            amount  = amount - bill.amount_paid
        print(f"Got Bill id as : {bill_id}")
        return render_template('user/payment.html',
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
        return redirect(url_for('user_home'))  # Redirect back to the dashboard

if(__name__ == "__main__"):
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        start_scheduler(app)
    app.run(debug=True);


