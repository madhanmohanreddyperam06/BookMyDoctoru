from datetime import datetime, time, date, timedelta
from app import db

class Slot(db.Model):
    __tablename__ = 'slots'
    
    id = db.Column(db.Integer, primary_key=True)
    shift_id = db.Column(db.Integer, db.ForeignKey('shifts.id'), nullable=False)
    token_number = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    is_booked = db.Column(db.Boolean, default=False, nullable=False)
    is_locked = db.Column(db.Boolean, default=False, nullable=False)  # For transactional locking
    locked_until = db.Column(db.DateTime)  # For automatic lock release
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    shift = db.relationship('Shift', back_populates='slots')
    appointment = db.relationship('Appointment', back_populates='slot', uselist=False, cascade='all, delete-orphan')
    
    # Composite indexes
    __table_args__ = (
        db.Index('idx_slot_shift_token', 'shift_id', 'token_number'),
        db.Index('idx_slot_availability', 'shift_id', 'is_booked', 'is_locked'),
        db.UniqueConstraint('shift_id', 'token_number', name='unique_shift_token'),
    )
    
    @property
    def time_display(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"
    
    @property
    def token_display(self):
        return f"Token #{self.token_number}"
    
    def is_available(self):
        """Check if slot is available for booking"""
        if self.is_booked or self.is_locked:
            return False
        
        # Check if lock has expired
        if self.locked_until and datetime.utcnow() > self.locked_until:
            self.is_locked = False
            self.locked_until = None
            db.session.add(self)
            # Don't commit here - let caller handle transaction
            return True
        
        return True
    
    def lock_slot(self, lock_duration_minutes=10):
        """Lock slot for transactional booking"""
        if self.is_available():
            self.is_locked = True
            self.locked_until = datetime.utcnow() + timedelta(minutes=lock_duration_minutes)
            db.session.add(self)
            # Don't commit here - let caller handle transaction
            return True
        return False
    
    def unlock_slot(self):
        """Unlock slot"""
        self.is_locked = False
        self.locked_until = None
        db.session.add(self)
        # Don't commit here - let caller handle transaction
    
    def book_slot(self):
        """Book the slot permanently"""
        if self.is_available():
            self.is_booked = True
            self.is_locked = False
            self.locked_until = None
            db.session.add(self)
            # Don't commit here - let caller handle transaction
            return True
        return False
    
    def release_slot(self):
        """Release the slot (cancel appointment)"""
        self.is_booked = False
        self.is_locked = False
        self.locked_until = None
        db.session.add(self)
        # Don't commit here - let caller handle transaction
    
    @classmethod
    def generate_slots_for_shift(cls, shift, slot_duration_minutes=15):
        """Generate time slots for a shift"""
        from datetime import datetime, timedelta
        
        slots = []
        current_time = datetime.combine(date.min, shift.start_time)
        end_time = datetime.combine(date.min, shift.end_time)
        token_number = 1
        
        while current_time + timedelta(minutes=slot_duration_minutes) <= end_time:
            slot_end = current_time + timedelta(minutes=slot_duration_minutes)
            
            slot = cls(
                shift_id=shift.id,
                token_number=token_number,
                start_time=current_time.time(),
                end_time=slot_end.time(),
                duration_minutes=slot_duration_minutes
            )
            slots.append(slot)
            
            current_time = slot_end
            token_number += 1
        
        return slots
    
    def __repr__(self):
        return f'<Slot {self.token_display} - {self.time_display}>'
