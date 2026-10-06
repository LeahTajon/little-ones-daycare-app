from extensions import db
from datetime import date, datetime

class Child(db.Model):
    __tablename__ = 'children'

    id = db.Column(db.Integer, primary_key=True)

    # Basic Information
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)

    # Address
    street = db.Column(db.String(150))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    zipcode = db.Column(db.String(20))

    # Enrollment Information
    class_name = db.Column(db.String(50))
    program_type = db.Column(db.String(50))
    days_attending = db.Column(db.String(100))
    enrolled_date = db.Column(db.Date)
    start_date = db.Column(db.Date)

    # Health / Notes
    allergies = db.Column(db.Text)
    medical_notes = db.Column(db.Text)
    notes = db.Column(db.Text)

    # Photo
    photo = db.Column(db.String(200))

    # Parents
    parents = db.relationship('Parent', backref='child', cascade='all, delete-orphan', lazy=True)

    # Authorized pickup
    pickups = db.relationship('AuthorizedPickup', backref='child', cascade='all, delete-orphan', lazy=True)

    @property
    def age_in_months(self):
        today = date.today()

        years = today.year - self.date_of_birth.year
        months = today.month - self.date_of_birth.month

        if today.day < self.date_of_birth.day:
            months -= 1

        if months < 0:
            years -= 1
            months += 12

        return years * 12 + months

    @property
    def age_display(self):
        months = self.age_in_months

        # Less than 1 year
        if months < 12:
            return f"{months} month{'s' if months != 1 else ''} old"

        # 1 year or older
        years = months // 12

        return f"{years} year{'s' if years != 1 else ''} old"

    def determine_class(self):

        months = self.age_in_months

        if months <= 12:
            return 'Infant'

        elif months <= 36:
            return 'Toddler'

        elif months <= 60:
            return 'Pre-K'

        else:
            return 'After School'
    
    def __repr__(self):
        return f'<Child {self.first_name} {self.last_name}>'

class Parent(db.Model):
    __tablename__ = 'parents'

    id = db.Column(db.Integer, primary_key=True)

    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)

    role = db.Column(db.String(20), nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    occupation = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f'<Parent {self.full_name}>'

class AuthorizedPickup(db.Model):
    __tablename__ = 'authorized_pickups'

    id = db.Column(db.Integer, primary_key=True)

    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)

    full_name = db.Column(db.String(100), nullable=False)
    relationship = db.Column(db.String(50))
    phone = db.Column(db.String(20))

    def __repr__(self):
        return f'<Pickup {self.full_name}>'

class DailyLog(db.Model):
    __tablename__ = 'daily_logs'

    id = db.Column(db.Integer, primary_key=True)

    child_id = db.Column(
        db.Integer,
        db.ForeignKey('children.id'),
        nullable=False
    )

    log_date = db.Column(db.Date, nullable=False)

    arrival_time = db.Column(db.Time)
    departure_time = db.Column(db.Time)

    notes = db.Column(db.Text)

    child = db.relationship(
        'Child',
        backref=db.backref(
            'daily_logs',
            cascade='all, delete-orphan'
        )
    )

    def __repr__(self):
        return f'<DailyLog {self.child_id} {self.log_date}>'

class DailyHealthCheck(db.Model):
    __tablename__ = 'daily_health_checks'

    id = db.Column(db.Integer, primary_key=True)

    daily_log_id = db.Column(
        db.Integer,
        db.ForeignKey('daily_logs.id'),
        nullable=False
    )

    temperature = db.Column(db.Float)
    symptoms = db.Column(db.Text)

    notes = db.Column(db.Text)

    daily_log = db.relationship(
        'DailyLog',
        backref = db.backref(
            'health_check',
            cascade='all, delete-orphan',
            uselist=False
        )
    )

class MealLog(db.Model):
    __tablename__ = 'meal_logs'

    id = db.Column(db.Integer, primary_key=True)

    daily_log_id = db.Column(
        db.Integer,
        db.ForeignKey('daily_logs.id'),
        nullable = False
    )

    meal_type = db.Column(db.String(20), nullable=False)
    time = db.Column(db.Time)
    food = db.Column(db.String(200))
    amount = db.Column(db.String(100))
    notes = db.Column(db.Text)

    daily_log = db.relationship(
        'DailyLog',
        backref=db.backref(
            'meal_logs',
            cascade='all, delete-orphan'
        )
    )

    def __repr__(self):
        return f'<MealLog {self.daily_log_id} {self.meal_type}>'


class BottleLog(db.Model):
    __tablename__ = 'bottle_logs'

    id = db.Column(db.Integer, primary_key=True)

    daily_log_id = db.Column(
        db.Integer,
        db.ForeignKey('daily_logs.id'),
        nullable=False
    )

    time = db.Column(db.Time, nullable=False)

    bottle_type = db.Column(db.String(50))

    amount_offered = db.Column(db.Float)

    notes = db.Column(db.Text)

    daily_log = db.relationship(
        'DailyLog',
        backref=db.backref(
            'bottle_logs',
            cascade='all, delete-orphan'
        )
    )

    def __repr__(self):
        return f'<BottleLog {self.daily_log_id} {self.time}>'

class NapLog(db.Model):
    __tablename__ = 'nap_logs'

    id = db.Column(db.Integer, primary_key=True)

    daily_log_id = db.Column(
        db.Integer,
        db.ForeignKey('daily_logs.id'),
        nullable=False
    )

    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time)

    notes = db.Column(db.Text)

    daily_log = db.relationship(
        'DailyLog',
        backref=db.backref(
            'nap_logs',
            cascade='all, delete-orphan'
        )
    )

    def __repr__(self):
        return f'<NapLog {self.daily_log_id} {self.start_time}>'


class DiaperLog(db.Model):
    __tablename__ = 'diaper_logs'

    id = db.Column(db.Integer, primary_key=True)

    daily_log_id = db.Column(
        db.Integer,
        db.ForeignKey('daily_logs.id'),
        nullable=False
    )

    time = db.Column(db.Time, nullable=False)
    diaper_type = db.Column(db.String(30), nullable=False)
    diaper_desc = db.Column(db.String(30))
    notes = db.Column(db.Text)

    daily_log = db.relationship(
        'DailyLog',
        backref=db.backref(
            'diaper_logs',
            cascade='all, delete-orphan'
        )
    )

    def __repr__(self):
        return f'<DiaperLog {self.daily_log_id} {self.time}>'

class PottyLog(db.Model):
   __tablename__ = 'potty_logs'

   id = db.Column(db.Integer, primary_key=True)

   # Daily Log
   daily_log_id = db.Column(
       db.Integer,
       db.ForeignKey('daily_logs.id'),
       nullable=False
   )

   # Potty Information
   time = db.Column(db.DateTime, nullable=False)

   potty_status = db.Column(db.String(30), nullable=False)
   # Wet, BM, Wet + BM 

   potty_method = db.Column(db.String(30), nullable=False)
   # Toilet, Diaper, Pull up, Training Potty

   potty_progress = db.Column(db.String(50), nullable=True)
   # Used Independently, Used with Assistance, 
   # Sat on Potty, Tried - No Result, Refused, Had an accident

   notes = db.Column(db.Text, nullable=True)

   # Relationship
   daily_log = db.relationship(
       'DailyLog',
       backref=db.backref(
           'potty_logs',
           cascade='all, delete-orphan'
       )
   )

   def __repr__(self):
       return f'<PottyLog {self.daily_log_id} {self.time}>'

class ActivityLog(db.Model):

    __tablename__ = 'activity_logs'

    id = db.Column(db.Integer, primary_key=True)

    daily_log_id = db.Column(
        db.Integer,
        db.ForeignKey('daily_logs.id'),
        nullable=False
    )

    time = db.Column(db.Time)

    activity = db.Column(db.String(200), nullable=False)

    notes = db.Column(db.Text)

    daily_log = db.relationship(
        'DailyLog',
        backref=db.backref(
            'activity_logs',
            cascade='all, delete-orphan'
        )
    )

    def __repr__(self):
        return f'<ActivityLog {self.daily_log_id} {self.activity}>'

class Event(db.Model):

    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    event_date = db.Column(db.Date, nullable=False)

    start_time = db.Column(db.Time, nullable=True)
    end_time = db.Column(db.Time, nullable=True)

    event_type = db.Column(db.String(50), nullable=True)

    class_name = db.Column(db.String(50), nullable=True)

    description = db.Column(db.Text, nullable=True)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    