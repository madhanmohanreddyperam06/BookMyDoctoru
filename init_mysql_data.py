#!/usr/bin/env python3
"""
MySQL Database Initialization for Doctor Appointment System
Initializes the MySQL database with tables and sample data
"""

import os
import sys
from datetime import datetime, timedelta, time
from app import create_app, db
from app.models import User, Admin, Doctor, Patient, Speciality, Shift, Slot, Appointment, Medicine

def init_mysql_database():
    """Initialize MySQL database with tables and sample data"""
    
    app = create_app()
    
    with app.app_context():
        try:
            print("🔧 Initializing MySQL database...")
            
            # Drop all tables (fresh start)
            print("🗑️  Dropping existing tables...")
            db.drop_all()
            print("✅ Existing tables dropped")
            
            # Create all tables
            print("📋 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Create specialities
            print("🏥 Creating medical specialities...")
            specialities_data = [
                {'name': 'General Medicine', 'description': 'General medical consultation and primary care'},
                {'name': 'Cardiology', 'description': 'Heart and cardiovascular system diseases'},
                {'name': 'Pediatrics', 'description': 'Medical care for infants, children, and adolescents'},
                {'name': 'Orthopedics', 'description': 'Bone and joint disorders and injuries'},
                {'name': 'Dermatology', 'description': 'Skin, hair, and nail disorders'}
            ]
            
            for spec_data in specialities_data:
                speciality = Speciality(**spec_data)
                db.session.add(speciality)
            
            db.session.commit()
            print(f"✅ Created {len(specialities_data)} specialities")
            
            # Create medicines
            print("💊 Creating medicines...")
            medicines_data = [
                {'name': 'Paracetamol', 'generic_name': 'Acetaminophen', 'strength': '500mg', 'description': 'Pain reliever and fever reducer'},
                {'name': 'Ibuprofen', 'generic_name': 'Ibuprofen', 'strength': '400mg', 'description': 'Anti-inflammatory and pain reliever'},
                {'name': 'Amoxicillin', 'generic_name': 'Amoxicillin', 'strength': '500mg', 'description': 'Antibiotic for bacterial infections'},
                {'name': 'Omeprazole', 'generic_name': 'Omeprazole', 'strength': '20mg', 'description': 'Proton pump inhibitor for acid reflux'},
                {'name': 'Salbutamol', 'generic_name': 'Albuterol', 'strength': '100mcg', 'description': 'Bronchodilator for asthma'}
            ]
            
            for med_data in medicines_data:
                medicine = Medicine(**med_data)
                db.session.add(medicine)
            
            db.session.commit()
            print(f"✅ Created {len(medicines_data)} medicines")
            
            # Create admin user
            print("👨‍💼 Creating admin user...")
            admin_user = User(
                email='admin@hospital.com',
                password='admin123',
                role='admin'
            )
            db.session.add(admin_user)
            db.session.flush()  # Get user ID without committing
            
            admin_profile = Admin(
                user_id=admin_user.id,
                first_name='System',
                last_name='Administrator',
                phone='+91 9110395993'
            )
            db.session.add(admin_profile)
            
            # Create doctor users
            print("👩‍⚕️ Creating doctor users...")
            doctors_data = [
                {
                    'email': 'dr.smith@hospital.com',
                    'password': 'doctor123',
                    'first_name': 'John',
                    'last_name': 'Smith',
                    'phone': '+91 9876543210',
                    'speciality_name': 'General Medicine',
                    'consultation_mode': 'online',
                    'qualifications': 'MBBS, MD (General Medicine)'
                },
                {
                    'email': 'dr.johnson@hospital.com',
                    'password': 'doctor123',
                    'first_name': 'Sarah',
                    'last_name': 'Johnson',
                    'phone': '+91 9876543211',
                    'speciality_name': 'Cardiology',
                    'consultation_mode': 'offline',
                    'qualifications': 'MBBS, MD (Cardiology)'
                },
                {
                    'email': 'dr.wilson@hospital.com',
                    'password': 'doctor123',
                    'first_name': 'Michael',
                    'last_name': 'Wilson',
                    'phone': '+91 9876543212',
                    'speciality_name': 'Pediatrics',
                    'consultation_mode': 'online',
                    'qualifications': 'MBBS, MD (Pediatrics)'
                },
                {
                    'email': 'dr.brown@hospital.com',
                    'password': 'doctor123',
                    'first_name': 'Emily',
                    'last_name': 'Brown',
                    'phone': '+91 9876543213',
                    'speciality_name': 'Orthopedics',
                    'consultation_mode': 'online',
                    'qualifications': 'MBBS, MS (Orthopedics)'
                },
                {
                    'email': 'dr.davis@hospital.com',
                    'password': 'doctor123',
                    'first_name': 'Robert',
                    'last_name': 'Davis',
                    'phone': '+91 9876543214',
                    'speciality_name': 'Dermatology',
                    'consultation_mode': 'online',
                    'qualifications': 'MBBS, MD (Dermatology)'
                }
            ]
            
            for doc_data in doctors_data:
                doctor_user = User(
                    email=doc_data['email'],
                    password=doc_data['password'],
                    role='doctor'
                )
                db.session.add(doctor_user)
                db.session.flush()
                
                speciality = Speciality.query.filter_by(name=doc_data['speciality_name']).first()
                doctor_profile = Doctor(
                    user_id=doctor_user.id,
                    first_name=doc_data['first_name'],
                    last_name=doc_data['last_name'],
                    phone=doc_data['phone'],
                    speciality=speciality,
                    consultation_mode=doc_data['consultation_mode'],
                    qualifications=doc_data['qualifications'],
                    consultation_fee=500.00
                )
                db.session.add(doctor_profile)
            
            db.session.commit()
            print(f"✅ Created {len(doctors_data)} doctors")
            
            # Create patient users
            print("👨‍⚕️ Creating patient users...")
            patients_data = [
                {
                    'email': 'patient1@email.com',
                    'password': 'patient123',
                    'first_name': 'Alice',
                    'last_name': 'Johnson',
                    'phone': '+91 9876543201',
                    'gender': 'female',
                    'date_of_birth': '1985-05-15',
                    'blood_group': 'A+'
                },
                {
                    'email': 'patient2@email.com',
                    'password': 'patient123',
                    'first_name': 'Bob',
                    'last_name': 'Smith',
                    'phone': '+91 9876543202',
                    'gender': 'male',
                    'date_of_birth': '1990-08-22',
                    'blood_group': 'B+'
                },
                {
                    'email': 'patient3@email.com',
                    'password': 'patient123',
                    'first_name': 'Carol',
                    'last_name': 'Williams',
                    'phone': '+91 9876543203',
                    'gender': 'female',
                    'date_of_birth': '1978-12-03',
                    'blood_group': 'O+'
                },
                {
                    'email': 'madhanmohanreddyperam06@gmail.com',
                    'password': 'patient123',
                    'first_name': 'MADHAN MOHAN REDDY',
                    'last_name': 'PERAM',
                    'phone': '+91 9110395993',
                    'gender': 'male',
                    'date_of_birth': '2004-04-29',
                    'blood_group': 'AB+'
                }
            ]
            
            for pat_data in patients_data:
                patient_user = User(
                    email=pat_data['email'],
                    password=pat_data['password'],
                    role='patient'
                )
                db.session.add(patient_user)
                db.session.flush()
                
                patient_profile = Patient(
                    user_id=patient_user.id,
                    first_name=pat_data['first_name'],
                    last_name=pat_data['last_name'],
                    phone=pat_data['phone'],
                    gender=pat_data['gender'],
                    date_of_birth=datetime.strptime(pat_data['date_of_birth'], '%Y-%m-%d').date(),
                    blood_group=pat_data['blood_group']
                )
                db.session.add(patient_profile)
            
            db.session.commit()
            print(f"✅ Created {len(patients_data)} patients")
            
            # Create sample shifts for next 7 days
            print("🕐 Creating doctor shifts...")
            doctors = Doctor.query.all()
            start_date = datetime.now().date()
            
            for doctor in doctors:
                for day_offset in range(7):
                    shift_date = start_date + timedelta(days=day_offset)
                    
                    # Create morning shift
                    morning_shift = Shift(
                        doctor_id=doctor.id,
                        date=shift_date,
                        start_time=time(9, 0),  # 9:00 AM
                        end_time=time(13, 0),   # 1:00 PM
                        shift_type='morning',
                        consultation_mode=doctor.consultation_mode,
                        is_active=True
                    )
                    db.session.add(morning_shift)
                    
                    # Create evening shift
                    evening_shift = Shift(
                        doctor_id=doctor.id,
                        date=shift_date,
                        start_time=time(14, 0),  # 2:00 PM
                        end_time=time(18, 0),    # 6:00 PM
                        shift_type='evening',
                        consultation_mode=doctor.consultation_mode,
                        is_active=True
                    )
                    db.session.add(evening_shift)
            
            db.session.commit()
            total_shifts = Shift.query.count()
            print(f"✅ Created {total_shifts} shifts for {len(doctors)} doctors")
            
            # Create slots for shifts
            print("⏰ Creating time slots...")
            shifts = Shift.query.all()
            
            for shift in shifts:
                if shift.shift_type == 'morning':
                    start_hour = 9
                    end_hour = 13
                else:  # evening
                    start_hour = 14
                    end_hour = 18
                
                current_time = time(start_hour, 0)  # Start time
                token_number = 1
                
                while True:
                    # Calculate end time for this slot
                    end_minutes = current_time.minute + 30
                    end_hour_slot = current_time.hour + (end_minutes // 60)
                    end_minute_slot = end_minutes % 60
                    
                    if end_hour_slot >= end_hour:
                        break
                    
                    slot_end_time = time(end_hour_slot, end_minute_slot)
                    
                    slot = Slot(
                        shift_id=shift.id,
                        token_number=token_number,
                        start_time=current_time,
                        end_time=slot_end_time,
                        duration_minutes=30,
                        is_available=True
                    )
                    db.session.add(slot)
                    
                    # Move to next slot
                    next_minutes = current_time.minute + 30
                    current_time = time(current_time.hour + (next_minutes // 60), next_minutes % 60)
                    token_number += 1
                    
                    # Break if we've reached the end time
                    if current_time.hour >= end_hour:
                        break
            
            db.session.commit()
            total_slots = Slot.query.count()
            print(f"✅ Created {total_slots} time slots")
            
            print("\n🎉 MySQL database initialization completed successfully!")
            print("\n📊 Database Summary:")
            print(f"   👥 Users: {User.query.count()}")
            print(f"   👨‍💼 Admins: {Admin.query.count()}")
            print(f"   👩‍⚕️ Doctors: {Doctor.query.count()}")
            print(f"   👨‍⚕️ Patients: {Patient.query.count()}")
            print(f"   🏥 Specialities: {Speciality.query.count()}")
            print(f"   💊 Medicines: {Medicine.query.count()}")
            print(f"   🕐 Shifts: {Shift.query.count()}")
            print(f"   ⏰ Slots: {Slot.query.count()}")
            
            print("\n🔑 Login Credentials:")
            print("   Admin: admin@hospital.com / admin123")
            print("   Doctors: dr.smith@hospital.com / doctor123")
            print("   Patients: patient1@email.com / patient123")
            print("   Your Account: madhanmohanreddyperam06@gmail.com / patient123")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error initializing database: {e}")
            sys.exit(1)

if __name__ == '__main__':
    init_mysql_database()
