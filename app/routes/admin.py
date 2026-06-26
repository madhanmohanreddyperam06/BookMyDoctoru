from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Admin, Doctor, Patient, Speciality, Shift, Slot, Appointment
from datetime import datetime, date, timedelta

admin = Blueprint('admin', __name__)

# Admin access decorator
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with overview statistics"""
    # Get statistics
    today = date.today()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    
    # Appointment statistics
    total_appointments_today = Appointment.query.filter_by(date=today).count()
    total_appointments_week = Appointment.query.filter(
        Appointment.date >= start_of_week,
        Appointment.date <= today
    ).count()
    total_appointments_month = Appointment.query.filter(
        Appointment.date >= start_of_month,
        Appointment.date <= today
    ).count()
    
    # User statistics
    total_doctors = Doctor.query.filter_by(is_active=True).count()
    total_patients = Patient.query.count()
    
    # Revenue statistics
    revenue_today = db.session.query(db.func.sum(Appointment.consultation_fee)).filter(
        Appointment.date == today,
        Appointment.payment_status == 'paid'
    ).scalar() or 0
    
    revenue_month = db.session.query(db.func.sum(Appointment.consultation_fee)).filter(
        Appointment.date >= start_of_month,
        Appointment.date <= today,
        Appointment.payment_status == 'paid'
    ).scalar() or 0
    
    # Recent appointments
    recent_appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_appointments_today=total_appointments_today,
                         total_appointments_week=total_appointments_week,
                         total_appointments_month=total_appointments_month,
                         total_doctors=total_doctors,
                         total_patients=total_patients,
                         revenue_today=revenue_today,
                         revenue_month=revenue_month,
                         recent_appointments=recent_appointments)

@admin.route('/doctors')
@login_required
@admin_required
def doctors():
    """Manage doctors"""
    page = request.args.get('page', 1, type=int)
    doctors = Doctor.query.join(Speciality).order_by(Doctor.last_name, Doctor.first_name).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('admin/doctors.html', doctors=doctors)

@admin.route('/doctors/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_doctor():
    """Add new doctor"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        speciality_id = request.form.get('speciality_id')
        consultation_mode = request.form.get('consultation_mode')
        consultation_fee = request.form.get('consultation_fee')
        experience_years = request.form.get('experience_years')
        qualifications = request.form.get('qualifications')
        
        # Validation
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('admin.add_doctor'))
        
        try:
            # Create user
            user = User(email=email, password=password, role='doctor')
            db.session.add(user)
            db.session.flush()
            
            # Create doctor profile
            doctor = Doctor(
                user_id=user.id,
                speciality_id=speciality_id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                consultation_mode=consultation_mode,
                consultation_fee=consultation_fee,
                experience_years=experience_years or None,
                qualifications=qualifications
            )
            db.session.add(doctor)
            db.session.commit()
            
            flash('Doctor added successfully!', 'success')
            return redirect(url_for('admin.doctors'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to add doctor. Please try again.', 'danger')
    
    specialities = Speciality.query.filter_by(is_active=True).all()
    return render_template('admin/add_doctor.html', specialities=specialities)

@admin.route('/specialities')
@login_required
@admin_required
def specialities():
    """Manage specialities"""
    specialities = Speciality.query.order_by(Speciality.name).all()
    total_doctors = sum(speciality.get_active_doctors_count() for speciality in specialities)
    avg_doctors_per_speciality = total_doctors / len(specialities) if specialities else 0
    return render_template('admin/specialities.html', specialities=specialities, total_doctors=total_doctors, avg_doctors_per_speciality=avg_doctors_per_speciality)

@admin.route('/specialities/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_speciality():
    """Add new speciality"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if Speciality.query.filter_by(name=name).first():
            flash('Speciality already exists', 'danger')
            return redirect(url_for('admin.add_speciality'))
        
        try:
            speciality = Speciality(name=name, description=description)
            db.session.add(speciality)
            db.session.commit()
            
            flash('Speciality added successfully!', 'success')
            return redirect(url_for('admin.specialities'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to add speciality. Please try again.', 'danger')
    
    return render_template('admin/add_speciality.html')

@admin.route('/shifts')
@login_required
@admin_required
def shifts():
    """Manage doctor shifts"""
    page = request.args.get('page', 1, type=int)
    shifts = Shift.query.join(Doctor).order_by(Shift.date.desc(), Shift.start_time).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/shifts.html', shifts=shifts)

@admin.route('/shifts/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_shift():
    """Add new doctor shift"""
    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        shift_date = request.form.get('date')
        start_time = request.form.get('start_time')
        end_time = request.form.get('end_time')
        shift_type = request.form.get('shift_type')
        consultation_mode = request.form.get('consultation_mode')
        max_patients = request.form.get('max_patients', 1, type=int)
        
        try:
            shift = Shift(
                doctor_id=doctor_id,
                date=datetime.strptime(shift_date, '%Y-%m-%d').date(),
                start_time=datetime.strptime(start_time, '%H:%M').time(),
                end_time=datetime.strptime(end_time, '%H:%M').time(),
                shift_type=shift_type,
                consultation_mode=consultation_mode,
                max_patients=max_patients
            )
            db.session.add(shift)
            db.session.flush()
            
            # Generate slots for the shift
            slot_duration = 15  # Default 15 minutes per slot
            slots = Slot.generate_slots_for_shift(shift, slot_duration)
            db.session.add_all(slots)
            
            db.session.commit()
            
            flash('Shift added successfully with slots!', 'success')
            return redirect(url_for('admin.shifts'))
            
        except Exception as e:
            db.session.rollback()
            flash('Failed to add shift. Please try again.', 'danger')
    
    doctors = Doctor.query.filter_by(is_active=True).all()
    return render_template('admin/add_shift.html', doctors=doctors)

@admin.route('/doctors/<int:doctor_id>/activate', methods=['POST'])
@login_required
@admin_required
def activate_doctor(doctor_id):
    """Activate a doctor"""
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_active = True
    db.session.commit()
    return jsonify({'success': True})

@admin.route('/doctors/<int:doctor_id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_doctor(doctor_id):
    """Deactivate a doctor"""
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.is_active = False
    db.session.commit()
    return jsonify({'success': True})

@admin.route('/specialities/<int:speciality_id>/activate', methods=['POST'])
@login_required
@admin_required
def activate_speciality(speciality_id):
    """Activate a speciality"""
    speciality = Speciality.query.get_or_404(speciality_id)
    speciality.is_active = True
    db.session.commit()
    return jsonify({'success': True})

@admin.route('/specialities/<int:speciality_id>/deactivate', methods=['POST'])
@login_required
@admin_required
def deactivate_speciality(speciality_id):
    """Deactivate a speciality"""
    speciality = Speciality.query.get_or_404(speciality_id)
    speciality.is_active = False
    db.session.commit()
    return jsonify({'success': True})

@admin.route('/shifts/<int:shift_id>/cancel', methods=['POST'])
@login_required
@admin_required
def cancel_shift(shift_id):
    """Cancel a shift"""
    shift = Shift.query.get_or_404(shift_id)
    shift.is_active = False
    db.session.commit()
    return jsonify({'success': True})
