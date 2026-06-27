#!/usr/bin/env python3
"""
Database Table Initialization for Doctor Appointment System
Creates all database tables using SQLAlchemy
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import app and models
from app import create_app, db
from app.models.user import User
from app.models.admin import Admin
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.models.speciality import Speciality
from app.models.shift import Shift
from app.models.slot import Slot
from app.models.appointment import Appointment
from app.models.prescription import Prescription
from app.models.medicine import Medicine

def create_tables():
    """Create all database tables"""
    
    try:
        print("🔧 Creating Flask application...")
        app = create_app()
        
        with app.app_context():
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ All tables created successfully!")
            
            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"\n📋 Created tables: {', '.join(tables)}")
            
            print("\n🎉 Database initialization completed!")
            print("\n📋 Next steps:")
            print("1. Run: python init_mysql_data.py to seed sample data")
            print("2. Run: python run.py to start the application")
            
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_tables()
