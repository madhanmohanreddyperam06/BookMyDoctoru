from datetime import datetime, date
from app import db

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    slot_id = db.Column(db.Integer, db.ForeignKey('slots.id'), nullable=False, unique=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    consultation_mode = db.Column(db.Enum('online', 'offline', name='consultation_mode'), nullable=False)
    status = db.Column(db.Enum('confirmed', 'completed', 'cancelled', 'no_show', name='appointment_status'), default='confirmed', nullable=False)
    consultation_fee = db.Column(db.Numeric(10, 2), nullable=False)
    payment_status = db.Column(db.Enum('pending', 'paid', 'refunded', name='payment_status'), default='pending', nullable=False)
    video_link = db.Column(db.String(500))  # For online consultations
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    slot = db.relationship('Slot', back_populates='appointment')
    doctor = db.relationship('Doctor', back_populates='appointments')
    patient = db.relationship('Patient', back_populates='appointments')
    prescription = db.relationship('Prescription', back_populates='appointment', uselist=False, cascade='all, delete-orphan')
    
    # Indexes for efficient querying
    __table_args__ = (
        db.Index('idx_appointment_doctor_date', 'doctor_id', 'date', 'status'),
        db.Index('idx_appointment_patient_date', 'patient_id', 'date', 'status'),
        db.Index('idx_appointment_status', 'status', 'date'),
    )
    
    @property
    def time_display(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    @property
    def status_display(self):
        return self.status.replace('_', ' ').title()
    
    @property
    def payment_status_display(self):
        return self.payment_status.replace('_', ' ').title()
    
    @property
    def token_number(self):
        return self.slot.token_number if self.slot else None
    
    @property
    def token_display(self):
        return f"Token #{self.token_number}" if self.token_number else "No Token"
    
    def can_be_cancelled(self):
        """Check if appointment can be cancelled"""
        if self.status in ['completed', 'cancelled', 'no_show']:
            return False
        
        # Check if it's too close to appointment time (e.g., within 2 hours)
        appointment_datetime = datetime.combine(self.date, self.start_time)
        current_datetime = datetime.utcnow()
        time_diff = appointment_datetime - current_datetime
        
        return time_diff.total_seconds() > 7200  # 2 hours in seconds
    
    def complete_appointment(self):
        """Mark appointment as completed"""
        if self.status == 'confirmed':
            self.status = 'completed'
            self.payment_status = 'paid'
            db.session.add(self)
            # Don't commit here - let caller handle transaction
            return True
        return False
    
    def cancel_appointment(self):
        """Cancel appointment and release slot"""
        if self.can_be_cancelled():
            self.status = 'cancelled'
            self.payment_status = 'refunded' if self.payment_status == 'paid' else 'cancelled'
            
            # Release the slot
            if self.slot:
                self.slot.release_slot()
            
            db.session.add(self)
            # Don't commit here - let caller handle transaction
            return True
        return False
    
    def mark_no_show(self):
        """Mark patient as no-show"""
        if self.status == 'confirmed':
            self.status = 'no_show'
            self.payment_status = 'cancelled'
            db.session.add(self)
            # Don't commit here - let caller handle transaction
            return True
        return False
    
    def add_video_link(self, video_link):
        """Add video consultation link for online appointments"""
        if self.consultation_mode == 'online' and video_link:
            self.video_link = video_link
            db.session.add(self)
            # Don't commit here - let caller handle transaction
            return True
        return False
    
    @classmethod
    def get_appointments_by_date_range(cls, start_date, end_date, doctor_id=None, status=None):
        """Get appointments within a date range with optional filters"""
        query = cls.query.filter(
            cls.date >= start_date,
            cls.date <= end_date
        )
        
        if doctor_id:
            query = query.filter(cls.doctor_id == doctor_id)
        
        if status:
            query = query.filter(cls.status == status)
        
        return query.order_by(cls.date, cls.start_time).all()
    
    @classmethod
    def get_today_appointments(cls, doctor_id=None):
        """Get today's appointments"""
        return cls.get_appointments_by_date_range(date.today(), date.today(), doctor_id)
    
    def __repr__(self):
        return f'<Appointment {self.patient.full_name} with {self.doctor.full_name} on {self.date} {self.time_display}>'
