from datetime import date
report_data = [
    {
        'due_date': date(2025, 1, 13),
        'monthly_rental': 15000.0,
        'amount_paid': 14000.0,
        'amount_due': 1000.0,
        'payment_date': date(2025, 1, 11),
        'payment_status': 'Partially Paid',
        'Tenant_Name': 'John Doe'
    },
    {
        'due_date': date(2025, 1, 14),
        'monthly_rental': 15000.0,
        'amount_paid': 15000.0,
        'amount_due': 0.0,
        'payment_date': date(2025, 1, 10),
        'payment_status': 'Fully Paid',
        'Tenant_Name': 'Jane Smith'
    },
    {
        'due_date': date(2025, 1, 15),
        'monthly_rental': 15000.0,
        'amount_paid': 0.0,
        'amount_due': 15000.0,
        'payment_date': None,
        'payment_status': 'Not Paid',
        'Tenant_Name': 'Michael Johnson'
    }
]

maintenance_records = [
    {"id": 1, "raised_by": "Tenant A", "description": "Leaky faucet in kitchen sink", "category": "Plumbing", "priority": "High","status_id":1 , "status": "In Progress"},
    {"id": 2, "raised_by": "Tenant B", "description": "Broken light switch in bedroom", "category": "Electrical", "priority": "Medium","status_id":2 ,  "status": "Pending"},
    {"id": 3, "raised_by": "Tenant C", "description": "Noisy AC unit in living room", "category": "HVAC", "priority": "Low","status_id":3 , "status": "Completed"},
    # ... other records
]

status_list = [
    {"status_id":1, "status_text":"In Progress"},
    {"status_id":2, "status_text":"Pending"},
    {"status_id":3, "status_text":"Complete"}
]