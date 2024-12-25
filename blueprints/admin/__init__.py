from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user, login_required
from flask_security import roles_accepted
from models import db
from models.agreement import Agreement
from models.property import Property
from models.apartment import Apartment
from models.maintenance import Maintenance
from models.user_model import User
from models.enums import StatusEnum
from models.bill import Bill
from datetime import date

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates')


@admin_bp.route('/home')
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
        'admin_home.html', 
        data=processed_data,   
        managed_properties_count= managed_properties_count,
        apartment_units_count=  apartment_units_count,
        tenants_count= tenants_count,
        active_maintenance_count=active_maintenance_count)

@admin_bp.route('/maintenance/update/<int:id>', methods=['POST'])
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