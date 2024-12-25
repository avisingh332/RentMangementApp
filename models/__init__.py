from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

# creating SQLAlchemy db class
db = SQLAlchemy()

def init_db(app):   
    with app.app_context():
        db.session.execute(text('PRAGMA foreign_keys = ON;'))
        from database.seed_data import seed
        db.create_all()
        seed(db)
        
