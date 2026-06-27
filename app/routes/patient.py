from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Patient, Doctor, Speciality, Shift, Slot, Appointment, Prescription
from datetime import datetime, date, timedelta

patient = Blueprint('patient', __name__)

# Patient access decorator
def patient_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_patient():
            flash('Patient access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@patient.route('/dashboard')
@login_required
@patient_required
def dashboard():
    """Patient dashboard"""
    patient_profile = current_user.patient
    
    # Get upcoming appointments
    upcoming_appointments = patient_profile.get_upcoming_appointments(limit=5)
    
    # Get past appointments
    past_appointments = patient_profile.get_past_appointments(limit=5)
    
    return render_template('patient/dashboard.html',
                         patient=patient_profile,
                         upcoming_appointments=upcoming_appointments,
                         past_appointments=past_appointments)

@patient.route('/doctors')
@login_required
@patient_required
def doctors():
    """Browse doctors"""
    consultation_mode = request.args.get('mode', 'all')
    speciality_filter = request.args.get('speciality', '')
    page = request.args.get('page', 1, type=int)
    
    query = Doctor.query.join(Speciality).filter(Doctor.is_active == True)
    
    # Filter by consultation mode
    if consultation_mode in ['online', 'offline']:
        query = query.filter(Doctor.consultation_mode == consultation_mode)
    
    # Filter by speciality
    if speciality_filter:
        query = query.filter(Speciality.name.ilike(f'%{speciality_filter}%'))
    
    doctors = query.order_by(Doctor.last_name, Doctor.first_name).paginate(
        page=page, per_page=10, error_out=False)
    
    specialities = Speciality.query.filter_by(is_active=True).order_by(Speciality.name).all()
    
    return render_template('patient/doctors.html',
                         doctors=doctors,
                         specialities=specialities,
                         consultation_mode=consultation_mode,
                         speciality_filter=speciality_filter)

@patient.route('/doctor/<int:doctor_id>')
@login_required
@patient_required
def doctor_detail(doctor_id):
    """View doctor details"""
    doctor = Doctor.query.filter_by(id=doctor_id, is_active=True).first_or_404()
    
    # Get available shifts for next 7 days
    start_date = date.today()
    end_date = start_date + timedelta(days=7)
    
    available_shifts = Shift.query.filter(
        Shift.doctor_id == doctor.id,
        Shift.date >= start_date,
        Shift.date <= end_date,
        Shift.is_active == True,
        Shift.consultation_mode == doctor.consultation_mode
    ).order_by(Shift.date, Shift.start_time).all()
    
    return render_template('patient/doctor_detail.html',
                         doctor=doctor,
                         available_shifts=available_shifts)

@patient.route('/book_appointment/doctor/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
@patient_required
def book_appointment(doctor_id):
    """Book appointment with doctor"""
    doctor = Doctor.query.filter_by(id=doctor_id, is_active=True).first_or_404()
    patient_profile = current_user.patient
    
    if request.method == 'POST':
        shift_id = request.form.get('shift_id')
        slot_id = request.form.get('slot_id')
        
        # Convert to integers for database query
        try:
            shift_id = int(shift_id) if shift_id else None
            slot_id = int(slot_id) if slot_id else None
        except (ValueError, TypeError):
            flash('Invalid shift or slot selected.', 'danger')
            return redirect(url_for('patient.book_appointment', doctor_id=doctor_id))
        
        shift = Shift.query.filter_by(id=shift_id, doctor_id=doctor.id).first_or_404()
        slot = Slot.query.filter_by(id=slot_id, shift_id=shift.id).first_or_404()
        
        # Check if slot is available
        if not slot.is_available():
            flash('This slot is no longer available. Please choose another slot.', 'danger')
            return redirect(url_for('patient.book_appointment', doctor_id=doctor_id))
        
        try:
            # Lock the slot for booking
            if slot.lock_slot():
                # Create appointment
                appointment = Appointment(
                    slot_id=slot.id,
                    doctor_id=doctor.id,
                    patient_id=patient_profile.id,
                    date=shift.date,
                    start_time=slot.start_time,
                    end_time=slot.end_time,
                    consultation_mode=doctor.consultation_mode,
                    consultation_fee=doctor.consultation_fee
                )
                db.session.add(appointment)
                db.session.flush()
                
                # Book the slot permanently
                slot.book_slot()
                
                db.session.commit()
                
                flash(f'Appointment booked successfully! {slot.token_display}', 'success')
                return redirect(url_for('patient.appointment_detail', appointment_id=appointment.id))
            else:
                flash('Failed to book slot. Please try again.', 'danger')
                return redirect(url_for('patient.book_appointment', doctor_id=doctor_id))
                
        except Exception as e:
            db.session.rollback()
            flash(f'Booking failed: {str(e)}', 'danger')
            return redirect(url_for('patient.book_appointment', doctor_id=doctor_id))
    
    # Get available shifts and slots
    start_date = date.today()
    end_date = start_date + timedelta(days=7)
    
    available_shifts = Shift.query.filter(
        Shift.doctor_id == doctor.id,
        Shift.date >= start_date,
        Shift.date <= end_date,
        Shift.is_active == True,
        Shift.consultation_mode == doctor.consultation_mode
    ).order_by(Shift.date, Shift.start_time).all()
    
    return render_template('patient/book_appointment.html',
                         doctor=doctor,
                         available_shifts=available_shifts)

@patient.route('/api/slots/<int:shift_id>')
@login_required
@patient_required
def get_slots(shift_id):
    """API endpoint to get available slots for a shift"""
    shift = Shift.query.filter_by(id=shift_id).first_or_404()
    
    slots = Slot.query.filter_by(shift_id=shift.id).order_by(Slot.token_number).all()
    
    slots_data = []
    for slot in slots:
        slots_data.append({
            'id': slot.id,
            'token': slot.token_number,
            'time': slot.time_display,
            'available': slot.is_available()
        })
    
    return jsonify({'slots': slots_data})

@patient.route('/appointments')
@login_required
@patient_required
def appointments():
    """View patient's appointments"""
    patient_profile = current_user.patient
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status')
    
    query = Appointment.query.filter_by(patient_id=patient_profile.id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    appointments = query.order_by(Appointment.date.desc(), Appointment.start_time.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('patient/appointments.html',
                         patient=patient_profile,
                         appointments=appointments,
                         status_filter=status_filter)

@patient.route('/appointment/<int:appointment_id>')
@login_required
@patient_required
def appointment_detail(appointment_id):
    """View appointment details"""
    patient_profile = current_user.patient
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        patient_id=patient_profile.id
    ).first_or_404()
    
    return render_template('patient/appointment_detail.html',
                         patient=patient_profile,
                         appointment=appointment)

@patient.route('/appointment/<int:appointment_id>/cancel', methods=['POST'])
@login_required
@patient_required
def cancel_appointment(appointment_id):
    """Cancel appointment"""
    patient_profile = current_user.patient
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        patient_id=patient_profile.id
    ).first_or_404()
    
    if appointment.cancel_appointment():
        flash('Appointment cancelled successfully.', 'success')
    else:
        flash('Cannot cancel this appointment. It may be too close to the appointment time or already completed.', 'danger')
    
    return redirect(url_for('patient.appointment_detail', appointment_id=appointment_id))

@patient.route('/medical_history')
@login_required
@patient_required
def medical_history():
    """View medical history"""
    patient_profile = current_user.patient
    
    # Get all prescriptions
    prescriptions = Prescription.query.filter_by(
        patient_id=patient_profile.id
    ).order_by(Prescription.created_at.desc()).all()
    
    # Get last appointment
    from app.models.appointment import Appointment
    last_appointment = Appointment.query.filter_by(
        patient_id=patient_profile.id
    ).order_by(Appointment.date.desc()).first()
    
    return render_template('patient/medical_history.html',
                         patient=patient_profile,
                         prescriptions=prescriptions,
                         last_appointment=last_appointment)

@patient.route('/prescription/<int:prescription_id>')
@login_required
@patient_required
def prescription_detail(prescription_id):
    """View prescription details"""
    patient_profile = current_user.patient
    prescription = Prescription.query.filter_by(
        id=prescription_id,
        patient_id=patient_profile.id
    ).first_or_404()
    
    return render_template('patient/prescription_detail.html',
                         patient=patient_profile,
                         prescription=prescription)
