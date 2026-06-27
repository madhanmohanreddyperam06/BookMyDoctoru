from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Admin, Doctor, Patient, Speciality
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=remember)
            flash('Login successful!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            # Redirect based on user role
            if user.is_admin():
                return redirect(url_for('admin.dashboard'))
            elif user.is_doctor():
                return redirect(url_for('doctor.dashboard'))
            elif user.is_patient():
                return redirect(url_for('patient.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html')

@auth.route('/register/patient', methods=['GET', 'POST'])
def register_patient():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone = request.form.get('phone')
        date_of_birth = request.form.get('date_of_birth')
        gender = request.form.get('gender')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('auth/register_patient.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'danger')
            return render_template('auth/register_patient.html')
        
        try:
            # Create user
            user = User(email=email, password=password, role='patient')
            db.session.add(user)
            db.session.flush()  # Get user ID without committing
            
            # Create patient profile
            from datetime import datetime
            patient = Patient(
                user_id=user.id,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                date_of_birth=datetime.strptime(date_of_birth, '%Y-%m-%d').date(),
                gender=gender
            )
            db.session.add(patient)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            return render_template('auth/register_patient.html')
    
    return render_template('auth/register_patient.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth.route('/landing')
def landing():
    """Landing page for non-authenticated users"""
    return render_template('auth/landing.html')

@auth.route('/profile')
@login_required
def profile():
    """User profile page"""
    user_profile = current_user.get_profile()

    return render_template('auth/profile.html',
                         user=current_user,
                         profile=user_profile)

@auth.route('/update-blood-group', methods=['POST'])
@login_required
def update_blood_group():
    """Update patient blood group"""
    if not current_user.is_patient():
        return jsonify({'success': False, 'message': 'Only patients can update blood group'}), 403

    data = request.get_json()
    blood_group = data.get('blood_group')

    if not blood_group:
        return jsonify({'success': False, 'message': 'Blood group is required'}), 400

    valid_blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    if blood_group not in valid_blood_groups:
        return jsonify({'success': False, 'message': 'Invalid blood group'}), 400

    try:
        patient = current_user.patient
        patient.blood_group = blood_group
        db.session.commit()
        return jsonify({'success': True, 'message': 'Blood group updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Failed to update blood group'}), 500
