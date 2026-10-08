import os
import calendar
import resend

from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_wtf.csrf import generate_csrf
from extensions import db

from werkzeug.utils import secure_filename
from datetime import date, datetime, time
from sqlalchemy import or_, func

from dotenv import load_dotenv

from pdf.daily_log_pdf import create_daily_log_pdf
from reports import (
    create_student_directory_pdf,
    create_students_by_class_pdf,
    create_enrollment_summary_pdf,
    create_daily_log_report_pdf,
    create_birthday_report_pdf,
    create_parent_contact_report_pdf,
    create_child_profile_pdf
)

from flask_mail import Mail, Message
from urllib.parse import quote

load_dotenv()

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

mail = Mail(app)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

resend.api_key = os.getenv('RESEND_API_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///littleones.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(
    app.root_path,
    'static',
    'uploads'
)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

from models import (
        Child, 
        Parent, 
        AuthorizedPickup, 
        DailyLog, 
        DailyHealthCheck, 
        BottleLog,
        MealLog,
        NapLog,
        DiaperLog,
        PottyLog,
        ActivityLog,
        Event
    )
from forms import (
        ChildForm, 
        PottyLogForm, 
        ActivityLogForm, 
        BottleLogForm, 
        MealLogForm,
        DiaperLogForm,
        NapLogForm,
        EventForm
    )

# Capitalize Names
def cap(text):
    return text.strip().title() if text else text

# Index 
@app.route('/')
def index():

    # Basic Statistics
    total_children = Child.query.count()

    infant_count = Child.query.filter_by(
        class_name='Toddler'
    ).count()

    toddler_count = Child.query.filter_by(
        class_name='Toddler'
    ).count()

    prek_count = Child.query.filter_by(
        class_name='Pre-K'
    ).count()

    afterschool_count = Child.query.filter_by(
        class_name='After School'
    ).count()

    # Today's Attendance
    today = date.today()

    present_today = DailyLog.query.filter(
        DailyLog.log_date == today,
        DailyLog.arrival_time.isnot(None)
    ).count()

    absent_today = max(
        total_children - present_today,
        0
    )

    # Upcoming events
    upcoming_events = (
        Event.query
        .filter(Event.event_date >= today)
        .order_by(
            Event.event_date.asc(),
            Event.start_time.asc()
        )
        .limit(5)
        .all()
    )

    # Upcoming Birthdays
    children = Child.query.all()

    upcoming_birthdays = []

    for child in children:

        birthday = child.date_of_birth.replace(
            year=today.year
        )

        if birthday < today:
            birthday = child.date_of_birth.replace(
                year=today.year + 1
            )

        upcoming_birthdays.append({
            'child': child,
            'birthday': birthday
        })

    upcoming_birthdays.sort(
        key=lambda item: item['birthday']
    )

    upcoming_birthdays = upcoming_birthdays[:5]


    return render_template(
        'index.html',

        today=today,

        total_children=total_children,

        present_today=present_today,
        absent_today=absent_today,

        infant_count=infant_count,
        toddler_count=toddler_count,
        prek_count=prek_count,
        afterschool_count=afterschool_count,

        upcoming_birthdays=upcoming_birthdays,
        upcoming_events=upcoming_events
    )

# Children
@app.route('/children')
def children():

    search = request.args.get('search','').strip()
    class_name = request.args.get('class_name', '').strip()
    page = request.args.get('page', 1, type=int)

    query = (
        Child.query
            .outerjoin(Parent)
            .outerjoin(AuthorizedPickup)
    )

    # Classroom filter
    if class_name:
        query = query.filter(
            Child.class_name == class_name
        )

    if search:
        search_term = f'%{search}%'

        query = query.filter(
            db.or_(

                # Child Information
                Child.first_name.ilike(search_term),
                Child.last_name.ilike(search_term),
                Child.gender.ilike(search_term),
                Child.class_name.ilike(search_term),
                Child.program_type.ilike(search_term),
                Child.days_attending.ilike(search_term),

                # Address
                Child.street.ilike(search_term),
                Child.city.ilike(search_term),
                Child.state.ilike(search_term),
                Child.zipcode.ilike(search_term),

                # Health / Notes
                Child.allergies.ilike(search_term),
                Child.medical_notes.ilike(search_term),
                Child.notes.ilike(search_term),

                # Parent Information
                Parent.role.ilike(search_term),
                Parent.full_name.ilike(search_term),
                Parent.occupation.ilike(search_term),
                Parent.phone_number.ilike(search_term),
                Parent.email.ilike(search_term),

                # Authorized Pickups
                AuthorizedPickup.full_name.ilike(search_term),
                AuthorizedPickup.relationship.ilike(search_term),
                AuthorizedPickup.phone.ilike(search_term)

            )
        )

    # Remove duplicates caused by joins
    query = query.distinct()

    # Alphabetical order
    query = query.order_by(
        Child.last_name,
        Child.first_name
    )

    # Pagination
    children = query.paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    return render_template(
        'children.html',
        children=children,
        search=search,
        class_name=class_name
    )

# Add Child
@app.route('/children/add', methods=['GET', 'POST'])
def add_child():

    form = ChildForm()

    if form.validate_on_submit():

        # Handle upload photo
        filename = None

        if form.photo.data:
            file = form.photo.data
            filename = secure_filename(file.filename)

            upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(upload_path)

        child = Child(
            first_name=cap(form.first_name.data),
            last_name=cap(form.last_name.data),
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,

            street=cap(form.street.data),
            city=cap(form.city.data),
            state=cap(form.state.data),
            zipcode=form.zipcode.data,

            
            program_type=form.program_type.data,
            days_attending=', '.join(form.days_attending.data),

            enrolled_date=form.enrolled_date.data,
            start_date=form.start_date.data,

            allergies=form.allergies.data,
            medical_notes=form.medical_notes.data,
            notes=form.notes.data,
            photo=filename
        )

        # Determine class
        child.class_name=child.determine_class()

        db.session.add(child)
        db.session.commit()

        # Father
        if form.father_name.data:
            father = Parent(
                child=child,
                role='Father',
                full_name=cap(form.father_name.data),
                occupation=cap(form.father_occupation.data),
                phone_number=form.father_phone.data,
                email=form.father_email.data
            )

            db.session.add(father)

        # Mother
        if form.mother_name.data:
            mother = Parent(
                child=child,
                role='Mother',
                full_name=cap(form.mother_name.data),
                occupation=cap(form.mother_occupation.data),
                phone_number=form.mother_phone.data,
                email=form.mother_email.data
            )

            db.session.add(mother)

        # Authorized Pickup 
        pickup_list = [
            (
                form.pickup1_name.data,
                form.pickup1_relationship.data,
                form.pickup1_phone.data
            ),

            (
                form.pickup2_name.data,
                form.pickup2_relationship.data,
                form.pickup2_phone.data
            ),

            (
                form.pickup3_name.data,
                form.pickup3_relationship.data,
                form.pickup3_phone.data
            )
        ]

        for name, relationship, phone in pickup_list:

            if name:
                pickup = AuthorizedPickup(
                    child=child,
                    full_name=cap(name),
                    relationship=cap(relationship),
                    phone=phone
                )

                db.session.add(pickup)

        db.session.commit()

        flash(
            f'{child.first_name} {child.last_name} was added successfully!', 'success'
        )

        return redirect(url_for('children'))

    return render_template(
        'add_child.html',
        form=form
    )

# Edit Child Details
@app.route('/children/<int:child_id>/edit', methods=['GET', 'POST'])
def edit_child(child_id):

    child = Child.query.get_or_404(child_id)

    form = ChildForm()

    # Load existing information
    if request.method == 'GET':

        # Child Information
        form.first_name.data = child.first_name
        form.last_name.data = child.last_name
        form.date_of_birth.data = child.date_of_birth
        form.gender.data = child.gender

        # Address
        form.street.data = child.street
        form.city.data = child.city
        form.state.data = child.state
        form.zipcode.data = child.zipcode

        # Program
        form.program_type.data = child.program_type
        form.enrolled_date.data = child.enrolled_date
        form.start_date.data = child.start_date


        # Days attending
        if child.days_attending:
            form.days_attending.data = [
            day.strip()
            for day in child.days_attending.split(',')
        ]
        else:
            form.days_attending.data = []

        # Medical Information
        form.allergies.data = child.allergies
        form.medical_notes.data = child.medical_notes
        form.notes.data = child.notes

        # Parent Information
        father = next(
            (parent for parent in child.parents if parent.role == 'Father'),
            None
        )
        
        mother = next(
            (parent for parent in child.parents if parent.role == 'Mother'),
            None
        )

        # Father
        if father:
            form.father_name.data = father.full_name
            form.father_occupation.data = father.occupation
            form.father_phone.data = father.phone_number
            form.father_email.data = father.email

        # Mother
        if mother:
            form.mother_name.data = mother.full_name
            form.mother_occupation.data = mother.occupation
            form.mother_phone.data = mother.phone_number
            form.mother_email.data = mother.email

        # Authorized Pickup Information

        pickups = child.pickups

        if len(pickups) > 0:
            form.pickup1_name.data = pickups[0].full_name
            form.pickup1_relationship.data = pickups[0].relationship
            form.pickup1_phone.data = pickups[0].phone

        if len(pickups) > 1:
            form.pickup2_name.data = pickups[1].full_name
            form.pickup2_relationship.data = pickups[1].relationship
            form.pickup2_phone.data = pickups[1].phone

        if len(pickups) > 2:
            form.pickup3_name.data = pickups[2].full_name
            form.pickup3_relationship.data = pickups[2].relationship
            form.pickup3_phone.data = pickups[2].phone

    # Save changes
    if form.validate_on_submit():

        # Child information
        child.first_name = form.first_name.data
        child.last_name = form.last_name.data
        child.date_of_birth = form.date_of_birth.data
        child.gender = form.gender.data

        # Address
        child.street = cap(form.street.data)
        child.city = cap(form.city.data)
        child.state = cap(form.state.data)
        child.zipcode = form.zipcode.data

        # Program & Enrollment
        child.class_name = child.determine_class()
        
        child.program_type = form.program_type.data
        child.enrolled_date = form.enrolled_date.data
        child.start_date = form.start_date.data

        # Days attending
        child.days_attending = ', '.join(form.days_attending.data)
            

        # Medical Information
        child.allergies = form.allergies.data
        child.medical_notes = form.medical_notes.data
        child.notes = form.notes.data

        # Parent Information
        father = next(
            (parent for parent in child.parents if parent.role == 'Father'),
            None
        )

        mother = next(
            (parent for parent in child.parents if parent.role == 'Mother'),
            None
        )

        # Father
        if form.father_name.data:

            if father:
                father.full_name = cap(form.father_name.data)
                father.occupation = cap(form.father_occupation.data)
                father.phone_number = form.father_phone.data
                father.email = form.father_email.data

            else:
                father = Parent(
                    child_id=child.id,
                    role='Father',
                    full_name=cap(form.father_name.data),
                    occupation=cap(form.father_occupation.data),
                    phone_number=form.father_phone.data,
                    email=form.father_email.data
                )

                db.session.add(father)

        elif father:
            db.session.delete(father)

        # Mother
        if form.mother_name.data:

            if mother:
                mother.full_name = cap(form.mother_name.data)
                mother.occupation = cap(form.mother_occupation.data)
                mother.phone_number = form.mother_phone.data
                mother.email = form.mother_email.data

            else:
                mother = Parent(
                    child_id=child.id,
                    role='Mother',
                    full_name=cap(form.mother_name.data),
                    occupation=cap(form.mother_occupation.data),
                    phone_number=form.mother_phone.data,
                    email=form.mother_email.data
                )

                db.session.add(mother)

        elif mother:
            db.session.delete(mother)

        # Authorized Pickups
        pickup_data = [
            (
                form.pickup1_name.data,
                form.pickup1_relationship.data,
                form.pickup1_phone.data
            ),
            (
                form.pickup2_name.data,
                form.pickup2_relationship.data,
                form.pickup2_phone.data
            ),
            (
                form.pickup3_name.data,
                form.pickup3_relationship.data,
                form.pickup3_phone.data
            )
        ]

        # Update existing pickups / create new ones
        for index, (name, relationship, phone) in enumerate(pickup_data):

            if index < len(child.pickups):

                pickup = child.pickups[index]

                if name:
                    pickup.full_name = cap(name)
                    pickup.relationship = cap(relationship)
                    pickup.phone = phone

                else:
                    db.session.delete(pickup)

            else:

                if name:
                    pickup = AuthorizedPickup(
                        child_id = child.id,
                        full_name = cap(name),
                        relationship=cap(relationship),
                        phone=phone
                    )

                    db.session.add(pickup)

        # Photo

        if form.photo.data and form.photo.data.filename:
        
            file = form.photo.data
        
            filename = secure_filename(file.filename)
        
            file.save(
                os.path.join(
                    app.config['UPLOAD_FOLDER'],
                    filename
                    )
            )
        
            child.photo = filename

        # Save everything
        db.session.commit()

        flash(
            f'{child.first_name} {child.last_name} was updated successfully!',
            'success'
        )

        return redirect(
            url_for(
                'child_details',
                child_id=child.id
            )
        )

    return render_template(
            'add_child.html',
            form=form,
            child=child,
            edit=True
        )

# View Child Details
@app.route('/children/<int:child_id>')
def child_details(child_id):

    child = Child.query.get_or_404(child_id)

    return render_template(
        'child_details.html',
        child=child
    )

# Child Profile PDF
@app.route('/children/<int:child_id>/pdf')
def child_profile_pdf(child_id):

    child = Child.query.get_or_404(child_id)

    file_path = os.path.join(
        app.config.get(
            'UPLOAD_FOLDER',
            'static/uploads'
        ),
        f'child_{child.id}_profile.pdf'
    )    

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    create_child_profile_pdf(
        file_path,
        child 
    )

    return send_file(
        file_path,
        as_attachment=False,
        mimetype='application/pdf'
    )


# Delete Child
@app.route('/children/<int:child_id>/delete', methods=['POST'])
def delete_child(child_id):

    child = Child.query.get_or_404(child_id)

    child_name = f'{child.first_name} {child.last_name}'

    db.session.delete(child)
    db.session.commit()

    flash(
        f'{child_name} was deleted successfully',
        'success'
    )

    return redirect(url_for('children'))

# Daily Log
@app.route('/daily-log')
def daily_log():

    # Selected date from the date picker
    selected_date_string = request.args.get('date')

    if selected_date_string:
        try:
            selected_date = datetime.strptime(
                selected_date_string,
                '%Y-%m-%d'
            ).date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # Get all children
    children = Child.query.order_by(
        Child.first_name,
        Child.last_name
    ).all()

    # Group children by class
    infants = []
    toddlers = []
    prek = []
    afterschool = []

    for child in children:

        class_name = child.determine_class()

        if class_name == 'Infant':
            infants.append(child)

        elif class_name == 'Toddler':
            toddlers.append(child) 

        elif class_name == 'Pre-K':
            prek.append(child)

        elif class_name == 'After School':
            afterschool.append(child)

    # Today's log counts
    bottle_count = (
        BottleLog.query
        .join(DailyLog)
        .filter(DailyLog.log_date == selected_date)
        .count()
    )

    meal_count = (
        MealLog.query
        .join(DailyLog)
        .filter(DailyLog.log_date == selected_date)
        .count()
    )

    nap_count = (
        NapLog.query
        .join(DailyLog)
        .filter(DailyLog.log_date == selected_date)
        .count()
    )

    diaper_count = (
        DiaperLog.query
        .join(DailyLog)
        .filter(DailyLog.log_date == selected_date)
        .count()
    )

    health_check_count = (
        DailyHealthCheck.query
        .join(DailyLog)
        .filter(DailyLog.log_date == selected_date)
        .count()
    )

    return render_template(
        'daily_log.html',

        selected_date=selected_date,

        infants=infants,
        toddlers=toddlers,
        prek=prek,
        afterschool=afterschool,

        bottle_count=bottle_count,
        meal_count=meal_count,
        nap_count=nap_count,
        diaper_count=diaper_count,
        health_check_count=health_check_count
    )

@app.route('/daily-log/class')
def daily_log_class():

    # Selected class
    selected_class = request.args.get('class')

    # Selected date
    date_string = request.args.get('date')

    if date_string:
        selected_date = datetime.strptime(
            date_string,
            '%Y-%m-%d'
        ).date()

    else:
        selected_date = date.today()

    # Valid class filters
    valid_classes = [
        'Infant',
        'Toddler',
        'Pre-K',
        'Afterschool'
    ]

    # Make sure the selected class is valid
    if selected_class not in valid_classes: 
        return redirect( url_for( 
                'daily_log', 
                date=selected_date.strftime('%Y-%m-%d') 
        ) )

    # Current page
    page = request.args.get(
        'page',
        1,
        type=int
    )

    # Get children in the selected class
    children = Child.query.filter_by(
        class_name = selected_class
    ).order_by(
        Child.last_name.asc(),
        Child.first_name.asc()
    ).paginate(
        page=page,
        per_page=12
    )

    return render_template(
        'daily_log_class.html',
        children=children,
        selected_class=selected_class,
        selected_date=selected_date
    )

@app.route('/daily-log/<int:child_id>')
def child_daily_log(child_id):

    child = Child.query.get_or_404(child_id)

    # --------------------------------
    # Selected date
    # --------------------------------

    date_string = request.args.get('date')

    if date_string:
        try:
            selected_date = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # --------------------------------
    # Helper
    # Convert time/datetime to datetime
    # for consistent timeline sorting
    # --------------------------------

    def timeline_datetime(value):

        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, time):
            return datetime.combine(
                selected_date,
                value
            )

        return value

    # --------------------------------
    # Get Daily Log for selected date
    # --------------------------------

    daily_log = DailyLog.query.filter_by(
        child_id=child.id,
        log_date=selected_date
    ).first()

    # --------------------------------
    # Build Timeline
    # --------------------------------

    timeline = []

    if daily_log:

        # -----------------------------
        # Health Check
        # No time
        # -----------------------------

        if daily_log.health_check:

            timeline.append({
                'type': 'health',
                'time': None,
                'log': daily_log.health_check
            })

        # -----------------------------
        # Bottle Logs
        # -----------------------------

        for bottle in daily_log.bottle_logs:

            timeline.append({
                'type': 'bottle',
                'time': timeline_datetime(bottle.time),
                'log': bottle
            })

        # -----------------------------
        # Meal Logs
        # -----------------------------

        for meal in daily_log.meal_logs:

            timeline.append({
                'type': 'meal',
                'time': timeline_datetime(meal.time),
                'log': meal
            })

        # -----------------------------
        # Diaper Logs
        # ----------------------------- 

        for diaper in daily_log.diaper_logs:  

            timeline.append({
                'type': 'diaper',
                'time': timeline_datetime(diaper.time),
                'log': diaper
            })

        # -----------------------------
        # Potty Logs
        # ----------------------------- 

        for potty in daily_log.potty_logs:

            timeline.append({
                'type': 'potty',
                'time': timeline_datetime(potty.time),
                'log': potty
            })


        # -----------------------------
        # Nap Logs
        # -----------------------------

        for nap in daily_log.nap_logs:
            timeline.append({
                'type': 'nap', 
                'time': timeline_datetime(nap.start_time), 
                'log': nap
            })

        # -----------------------------
        # Activity Logs
        # -----------------------------

        for activity in daily_log.activity_logs:
            timeline.append({
                'type': 'activity',
                'time': timeline_datetime(activity.time),
                'log': activity
            })
    # --------------------------------
    # Separate timed and non-timed logs
    # --------------------------------

    health_items = [
        item for item in timeline
        if item['time'] is None
    ]

    timed_items = [
        item for item in timeline
        if item['time'] is not None
    ]

    # --------------------------------
    # Sort timed logs
    # Latest time FIRST
    # --------------------------------

    timed_items.sort(
        key=lambda item: item['time'],
        reverse=True
    )

    # --------------------------------
    # Final Timeline
    #
    # Latest activity
    #       ↓
    # Older activity
    #       ↓
    # Health Check
    # --------------------------------

    timeline = timed_items + health_items

    # --------------------------------
    # Summary
    # --------------------------------

    entries_count = len(timeline)

    if timed_items:
        last_activity = timed_items[0]['time']
    else:
        last_activity = None

    # --------------------------------
    # Render page
    # --------------------------------

    return render_template(
        'child_daily_log.html',
        child=child,
        daily_log=daily_log,
        selected_date=selected_date,
        timeline=timeline,
        entries_count=entries_count,
        last_activity=last_activity
    )

# Add Health Check
@app.route('/daily-log/<int:child_id>/health-check', methods=['GET', 'POST'])
def add_health_check(child_id):

    child = Child.query.get_or_404(child_id)

    # Get selected date
    date_string = request.args.get('date')

    if date_string:
        selected_date = datetime.strptime(
            date_string,
            '%Y-%m-%d'
        ).date()
    else:
        selected_date = date.today()

    # Find today's daily log for this child
    daily_log = DailyLog.query.filter_by(
        child_id = child.id,
        log_date = selected_date
    ).first()

    # Create DailyLog if it doesn't exist
    if not daily_log:

        daily_log = DailyLog(
            child_id=child.id,
            log_date=selected_date
        )

        db.session.add(daily_log)
        db.session.commit()

    if request.method == 'POST':

        temperature = request.form.get('temperature')
        symptoms = request.form.get('symptoms')
        notes = request.form.get('notes')

        # Convert temperature to float
        if temperature:
            try:
                temperature = float(temperature)
            except ValueError:
                flash(
                    'Please enter a valid temperature.',
                    'danger'
                )

                return render_template(
                    'add_health_check.html',
                    child=child,
                    daily_log=daily_log,
                    selected_date=selected_date
                )
        else:
            temperature=None

        health_check = DailyHealthCheck(
            daily_log_id=daily_log.id,
            temperature=temperature,
            symptoms=symptoms,
            notes=notes
        )

        db.session.add(health_check)
        db.session.commit()

        flash(
            'Daily health check added successfully.',
            'success'
        )

        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    return render_template(
        'add_health_check.html',
        child=child,
        daily_log=daily_log,
        selected_date=selected_date
    )

# Edit Health Check
@app.route('/daily-log/<int:child_id>/health-check/<int:log_id>/edit', methods=['GET', 'POST'])
def edit_health_check(child_id, log_id):

    child = Child.query.get_or_404(child_id)

    # Get the existing health check
    health_check = DailyHealthCheck.query.get_or_404(log_id)

    # Make sure this health check belongs to this child
    daily_log = DailyLog.query.filter_by(
        id=health_check.daily_log_id,
        child_id=child.id
    ).first_or_404()

    selected_date = daily_log.log_date

    # Save changes
    if request.method == 'POST':

        temperature = request.form.get('temperature')
        symptoms = request.form.get('symptoms')
        notes = request.form.get('notes')

        # Convert temperature to float
        if temperature:
            try:
                temperature = float(temperature)

            except ValueError:

                flash(
                    'Please enter a valid temperature.',
                    'danger'
                )

                return render_template(
                    'edit_health_check.html',
                    child=child,
                    health_check=health_check,
                    selected_date=selected_date
                )

        else:

            temperature = None

        # Update existing health check
        health_check.temperature = temperature
        health_check.symptoms = symptoms
        health_check.notes = notes

        db.session.commit()

        flash(
            'Health check updated successfully.',
            'success'
        )

        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    return render_template(
        'edit_health_check.html',
        child=child,
        health_check=health_check,
        selected_date=selected_date
    )
        
# Add Bottle Log
@app.route('/daily-log/<int:child_id>/bottle', methods=['GET', 'POST'])
def add_bottle_log(child_id):

    child = Child.query.get_or_404(child_id)

    form = BottleLogForm()

    # Selected date
    date_string = request.args.get('date')

    if date_string:
        try:
            selected_date = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()
        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # Current time for display
    current_time = datetime.now().strftime(
        '%I:%M %p'
    ).lstrip('0')

    # Submit
    if form.validate_on_submit():

        # Time
        if form.time_option.data == 'automatic':
            bottle_time = datetime.now().time().replace(
                second=0,
                microsecond=0
            )
        else:
            bottle_time = form.manual_time.data

        # Bottle type
        if form.bottle_type.data == 'other':

            bottle_type = (
                form.other_bottle.data or ''
            ).strip()

        else:

            bottle_choices = dict(
                form.bottle_type.choices
            )

            bottle_type = bottle_choices.get(
                form.bottle_type.data,
                form.bottle_type.data
            )

        # Find Daily Log
        daily_log = DailyLog.query.filter_by(
            child_id=child.id,
            log_date=selected_date
        ).first()

        # Create Daily Log if needed
        if not daily_log:

            daily_log = DailyLog(
                child_id=child.id,
                log_date=selected_date
            )

            db.session.add(daily_log)
            db.session.flush()

        # Create Bottle Log
        bottle_log = BottleLog(
            daily_log_id = daily_log.id,
            time=bottle_time,
            bottle_type=bottle_type,
            amount_offered=form.amount_offered.data,
            notes=form.notes.data
        )

        db.session.add(bottle_log)
        db.session.commit()

        flash(
            'Bottle log added successfully!',
            'success'
        )

        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    # Display form
    return render_template(
        'add_bottle_log.html',
        child=child,
        form=form,
        selected_date=selected_date,
        current_time=current_time
    )

# Edit Bottle Log
@app.route('/daily-log/<int:child_id>/bottle/<int:log_id>/edit', methods=['GET', 'POST'])
def edit_bottle_log(child_id, log_id):

    child = Child.query.get_or_404(child_id)

    # Get the actual BottleLog
    bottle_log = BottleLog.query.get_or_404(log_id)

    # Make sure this bottle log belongs to this child
    daily_log = DailyLog.query.filter_by(
        id=bottle_log.daily_log_id,
        child_id=child.id
    ).first_or_404()

    selected_date = daily_log.log_date

    form = BottleLogForm()

    # Load existing values

    if request.method == 'GET':

        # Time
        form.time_option.data = 'manual'
        form.manual_time.data = bottle_log.time

        # Bottle Type
        match_bottle_type = False

        for value, label in form.bottle_type.choices:

            if label == bottle_log.bottle_type:
                form.bottle_type.data = value
                match_bottle_type = True
                break

        # If it isn't one of the standard choices,
        # treat it as "Other"
        if not match_bottle_type:

            form.bottle_type.data = 'other'

            form.other_bottle.data = (
                bottle_log.bottle_type or ''
            )

        # Amount Offered
        form.amount_offered.data = (
            bottle_log.amount_offered
        )

        # Notes
        form.notes.data = (
            bottle_log.notes or ''
        )

    # Save Changes
    if form.validate_on_submit():

        # Time
        if form.time_option.data == 'automatic':

            # Keep the original time when
            # Automatic is selected while editing
            bottle_time = bottle_log.time

        else:

            bottle_time = form.manual_time.data

        # Bottle Type
        if form.bottle_type.data == 'other':

            bottle_type = (
                form.other_bottle.data or ''
            ).strip()

        else:

            bottle_choices = dict(
                form.bottle_type.choices
            )

            bottle_type = bottle_choices.get(
                form.bottle_type.data,
                form.bottle_type.data
            )

        # Update database record
        bottle_log.time = bottle_time

        bottle_log.bottle_type = bottle_type

        bottle_log.amount_offered = (
            form.amount_offered.data
        )

        bottle_log.notes = (
            form.notes.data
        )

        db.session.commit()

        flash(
            'Bottle log updated successfully!',
            'success'
        )

        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime(
                    '%Y-%m-%d'
                )
            )
        )

    current_time = datetime.now().strftime(
        '%I:%M %p'
    ).lstrip('0')

    return render_template(
        'edit_bottle_log.html',
        child=child,
        form=form,
        selected_date=selected_date,
        current_time=current_time,
        bottle_log=bottle_log
    )

# Add Meal Log
@app.route('/daily-log/<int:child_id>/meal', methods=['GET', 'POST'])
def add_meal_log(child_id):

    child = Child.query.get_or_404(child_id)

    # Selected Date
    date_string = request.args.get('date')

    if date_string:

        try:
            selected_date = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()

        except ValueError:
            selected_date = date.today()

    else:
        selected_date = date.today()

    # Find Daily Log

    daily_log = DailyLog.query.filter_by(
        child_id=child.id,
        log_date=selected_date
    ).first()

    # Create Daily Log if it doesn't exist
    if not daily_log:
        daily_log = DailyLog(
            child_id=child.id,
            log_date=selected_date
        )

        db.session.add(daily_log)
        db.session.commit()

    # Meal Form
    form = MealLogForm()

    # Submit Form

    if form.validate_on_submit():

        # Food
        selected_foods = form.food.data or []

        food_choices = dict(form.food.choices)

        food_names = [
            food_choices.get(value, value)
            for value in selected_foods
        ]

        # Other Food
        if form.other_food.data:

            other_food = form.other_food.data.strip()

            if other_food:
                food_names.append(other_food)

        # Combine foods into one string
        food_text = ', '.join(food_names)

        # Time
        if form.time_option.data == 'manual':

            # TimeField already gives us a datetime.time object
            meal_time = form.manual_time.data

        else:

            # Automatic time
            meal_time = datetime.now().time()

        # Create Meal Log
        meal = MealLog(
            daily_log_id=daily_log.id,
            meal_type=form.meal_type.data,
            time=meal_time,
            food=food_text,
            amount=form.amount.data,
            notes=form.notes.data
        )

        db.session.add(meal)
        db.session.commit()

        # Success message
        flash(
            'Meal log added successfully',
            'success'
        )

        # Return to daily log
        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    # Display Form
    return render_template(
        'add_meal_log.html',
        child=child,
        daily_log=daily_log,
        selected_date=selected_date,
        form=form
    )

# Edit Meal Log
@app.route('/daily-log/<int:child_id>/meal/<int:log_id>/edit', methods=['GET', 'POST'])
def edit_meal_log(child_id, log_id):

    child = Child.query.get_or_404(child_id)

    # Get the actual MealLog
    meal_log = MealLog.query.get_or_404(log_id)

    # Make sure this meal belongs to this child
    daily_log = DailyLog.query.filter_by(
        id=meal_log.daily_log_id,
        child_id=child.id
    ).first_or_404()

    selected_date = daily_log.log_date

    form = MealLogForm()

    # Load existing values

    if request.method == 'GET':

        # Meal Type
        form.meal_type.data = meal_log.meal_type

        # Time
        form.time_option.data = 'manual'
        form.manual_time.data = meal_log.time

        # Food
        food_choices = dict(form.food.choices)

        selected_foods = []
        other_foods = None

        if meal_log.food:

            saved_foods = [
                food.strip()
                for food in meal_log.food.split(',')
            ]

            for food in saved_foods:

                # Find the form value that matches
                # the saved label
                matched_value = next(
                    (
                        value 
                        for value, label in form.food.choices
                        if label == food
                    ),
                    None
                )

                if matched_value:
                    selected_foods.append(matched_value)

                else:
                    # Anything not matching a standard
                    # choice is treated as Other
                    other_food = food

        form.food.data = selected_foods
        form.other_food.data = other_food or ''

        # Amount
        form.amount.data = meal_log.amount

        # Notes
        form.notes.data = meal_log.notes or ''

    # Save changes

    if form.validate_on_submit():

        # Time
        if form.time_option.data == 'automatic':

            # Keep original time when editing
            meal_time = meal_log.time

        else:

            meal_time = form.manual_time.data

        # Food
        selected_foods = form.food.data or []

        food_choices = dict(form.food.choices)

        food_names = [
            food_choices.get(value, value)
            for value in selected_foods
        ]

        # Other Food
        if form.other_food.data:

            other_food = form.other_food.data.strip()

            if other_food:
                food_names.append(other_food)

        food_text = ', '.join(food_names)

        # Update Meal Log
        meal_log.meal_type = form.meal_type.data
        meal_log.time = meal_time
        meal_log.food = food_text
        meal_log.amount = form.amount.data
        meal_log.notes = form.notes.data

        db.session.commit()

        flash(
            'Meal log updated successfully!',
            'success'
        )    

        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    # Display form
    current_time = datetime.now().strftime(
        '%I:%M %p '
    ).lstrip('0')

    return render_template(
        'edit_meal_log.html',
        child=child,
        form=form,
        selected_date=selected_date,
        current_time=current_time,
        meal_log=meal_log
    )

# Add Diaper Log
@app.route('/daily-log/<int:child_id>/diaper', methods=['GET', 'POST'])
def add_diaper_log(child_id):

    child = Child.query.get_or_404(child_id)

    # Selected Date
    date_string = request.args.get('date')

    if date_string:
        try:
            selected_date = datetime.strptime(
                date_string,
                 '%Y-%m-%d'
            ).date()

        except ValueError:
            selected_date = date.today()

    else:
        selected_date = date.today()

    # Form
    form = DiaperLogForm()

    # Submit
    if form.validate_on_submit():

        # Determine Time
        if form.time_mode.data == 'automatic':

            log_time = datetime.now().time()

        else:
            log_time = form.manual_time.data

        # Find existing
        daily_log = DailyLog.query.filter_by(
            child_id=child.id,
            log_date=selected_date
        ).first()
        

        # Create Daily Log
        if not daily_log:
            daily_log = DailyLog(
                child_id=child.id,
                log_date=selected_date
            )

            db.session.add(daily_log)
            db.session.flush()

        # Create Diaper Log
        diaper_log = DiaperLog(
            daily_log_id=daily_log.id,
            diaper_type=form.diaper_type.data,
            diaper_desc=form.diaper_desc.data,
            notes=form.notes.data,
            time=log_time
        )

        db.session.add(diaper_log)
        db.session.commit()

        # Success
        flash(
            'Diaper log saved succesfully.',
            'success'
        )

        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    # Render
    return render_template(
        'add_diaper_log.html',
        child=child,
        selected_date=selected_date,
        form=form
    )

# Edit Diaper Log
@app.route('/daily-log/<int:child_id>/diaper/<int:log_id>/edit', methods=['GET', 'POST'])
def edit_diaper_log(child_id, log_id):

    child = Child.query.get_or_404(child_id)

    # Get the actual DiaperLog
    diaper_log = DiaperLog.query.get_or_404(log_id)

    # Make sure this diaper log belongs to this child
    daily_log = DailyLog.query.filter_by(
        id=diaper_log.daily_log_id,
        child_id=child.id
    ).first_or_404()

    selected_date = daily_log.log_date

    # Form
    form = DiaperLogForm()

    # Load existing values
    if request.method == 'GET':

        # Diaper Type
        form.diaper_type.data = diaper_log.diaper_type

        # Description
        form.diaper_desc.data = diaper_log.diaper_desc or ''

        # Notes
        form.notes.data = diaper_log.notes or ''

        # Time
        # Show the existing time in the manual time field
        form.time_mode.data = 'manual'
        form.manual_time.data = diaper_log.time

    # Save changes
    if form.validate_on_submit():

        # Time
        if form.time_mode.data == 'automatic':

            # Keep the original time when editing
            log_time = diaper_log.time

        else:

            log_time = form.manual_time.data 

        # Update Diaper Log
        diaper_log.diaper_type = form.diaper_type.data
        diaper_log.diaper_desc = form.diaper_desc.data
        diaper_log.notes = form.notes.data 
        diaper_log.time = log_time

        db.session.commit()

        # Success
        flash(
            'Diaper log updated successfully!',
            'success'
        )

        # return to Daily Log
        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    # Current time
    current_time = datetime.now().strftime(
        '%I:%M %p'
    ).lstrip('0')

    # Display form
    return render_template(
        'edit_diaper_log.html',
        child=child,
        form=form,
        selected_date=selected_date,
        current_time=current_time,
        diaper_log=diaper_log
    )
            
# Add Nap Log
@app.route('/daily-log/<int:child_id>/nap', methods=['GET', 'POST']) 
def add_nap(child_id):

    child = Child.query.get_or_404(child_id)

    date_string = request.args.get('date')

    if date_string:

        try:
            selected_date = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()

        except ValueError:

            selected_date = datetime.today().date()

    # Find Daily Log
    daily_log = DailyLog.query.filter_by(
        child_id=child.id,
        log_date=selected_date
    ).first()

    # Create Daily Log if it doesn't exist
    if not daily_log:

        daily_log = DailyLog(
            child_id=child.id,
            log_date=selected_date
        )

        db.session.add(daily_log)

        # Get the new DailyLog ID
        db.session.flush()

    # Find Active Nap
    active_nap = NapLog.query.filter_by(
        daily_log_id=daily_log.id,
        end_time=None
    ).first()

    # Form
    form = NapLogForm()

    # POST
    if form.validate_on_submit():
        action = request.form.get('action')

        # Start Nap
        if action == 'start':

            if active_nap:

                flash(
                    'A nap is already in progress.',
                    'warning'
                )

                return redirect(url_for(
                    'add_nap',
                    child_id=child.id,
                    date=selected_date.strftime('%Y-%m-%d')
                ))

            # Determine start time

            if form.time_mode.data == 'automatic':

                start_time = datetime.now().time().replace(
                    second=0,
                    microsecond=0
                )

            else:

                if not form.nap_time.data:

                    flash(
                        'Please enter the nap start time.',
                        'warning'
                    )

                    return redirect(url_for(
                        'add_nap',
                        child_id=child.id,
                        date=selected_date.strftime('%Y-%m-%d')
                    ))

                start_time = form.nap_time.data

            # Create Nap
            nap = NapLog(
                daily_log_id = daily_log.id,
                start_time=start_time,
                end_time=None
            )

            db.session.add(nap)
            db.session.commit()

            flash(
                'Nap started successfully.',
                'success'
            )

        # End Nap
        elif action == 'end':

            if not active_nap:

                flash(
                    'There is no active nap to end.',
                    'warning'
                )

                return redirect(url_for(
                    'add_nap',
                    child_id=child.id,
                    date=selected_date.strftime('%Y-%m-%d')
                ))

            # Determine end time
            if form.time_mode.data == 'automatic':

                end_time = datetime.now().time().replace(
                    second=0,
                    microsecond=0
                )

            else:

                if not form.nap_time.data:

                    flash(
                        'Please enter the nap end time.',
                        'warning'
                    )

                    return redirect(url_for(
                        'add_nap',
                        child_id=child.id,
                        date=selected_date.strftime('%Y-%m-%d')
                    ))

                end_time = form.nap_time.data 

            # Save end time
            active_nap.end_time = end_time

            db.session.commit()

            flash(
                'Nap ended successfully.',
                'success'
            )

        # Return to Daily Log
        return redirect(url_for(
            'child_daily_log',
            child_id=child.id,
            date=selected_date.strftime('%Y-%m-%d')
        ))

    # Render
    return render_template(
        'add_nap.html',
        child=child,
        selected_date=selected_date,
        active_nap=active_nap,
        form=form
    )

# Edit Nap Log
@app.route('/daily-log/<int:child_id>/nap/<int:log_id>/edit', methods=['GET', 'POST'])
def edit_nap_log(child_id, log_id):

    child = Child.query.get_or_404(child_id)

    # Get the actual Naplog
    nap_log = NapLog.query.get_or_404(log_id)

    # Make sure this nap belongs to this child
    daily_log = DailyLog.query.filter_by(
        id=nap_log.daily_log_id,
        child_id=child.id
    ).first_or_404()

    selected_date = daily_log.log_date

    # Form 
    form = NapLogForm()

    # Load existing values

    if request.method == 'GET':

        # Show existing start time
        form.start_time.data = nap_log.start_time

        # Show existing end time
        form.end_time.data = nap_log.end_time

        

    # Save changes
    if form.validate_on_submit():

        start_time = form.start_time.data
        end_time = form.end_time.data 

        if not start_time:
            flash(
                'Please enter the nap start time.',
                'warning'
            )

        elif end_time and end_time < start_time:
            flash(
                'Nap end time cannot be earlier than the start time.',
                'warning'
            )
        else:
            nap_log.start_time = start_time
            nap_log.end_time = end_time

            db.session.commit()

            flash(
                'Nap log updated successfully!',
                'success'
            )

            return redirect(
                url_for(
                    'child_daily_log',
                    child_id=child.id,
                    date=selected_date.strftime('%Y-%m-%d')
                )
            )
        
    # Current time
    current_time = datetime.now().strftime(
        '%I:%M %p'
    ).lstrip('0')

    # Display Edit Page
    return render_template(
        'edit_nap_log.html',
        child=child,
        form=form,
        selected_date=selected_date,
        current_time=current_time,
        nap_log=nap_log
    )
 
# Add Potty Log
@app.route('/daily-log/<int:child_id>/potty', methods=['GET', 'POST'])
def add_potty_log(child_id):

    child = Child.query.get_or_404(child_id)

    # Selected Date
    date_string = request.args.get('date')

    if date_string:
        try:
            selected_date = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()

        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # Get Daily Log for Selected Date
    daily_log = DailyLog.query.filter_by(
        child_id=child.id,
        log_date=selected_date
    ).first()

    # Create Daily Log if it doesn't exist
    if not daily_log:

        daily_log = DailyLog(
            child_id=child.id,
            log_date=selected_date
        )

        db.session.add(daily_log)
        db.session.commit()

    # Form
    form = PottyLogForm()

    # Submit Form
    if form.validate_on_submit():

        # Determine Potty Time
        if form.time_mode.data == 'manual':

            # Manual time is required
            if not form.manual_time.data:

                form.manual_time.errors.append(
                    'Please enter the potty time.'
                )

                return render_template(
                    'add_potty_log.html',
                    form=form,
                    child=child,
                    daily_log=daily_log,
                    selected_date=selected_date
                )

            # Combine selected date + manual time
            potty_time = datetime.combine(
                selected_date,
                form.manual_time.data
            )

        else:

            # Automatic time
            potty_time = datetime.now()

        # Create Potty Log
        potty_log = PottyLog(
            daily_log_id=daily_log.id,
            time=potty_time,
            potty_status=form.potty_status.data,
            potty_method=form.potty_method.data,
            potty_progress=form.potty_progress.data,
            notes=form.notes.data
        )

        db.session.add(potty_log)
        db.session.commit()

        # Success Message
        flash(
            'Potty log added successfully!',
            'success'
        )

        # Return to Daily Log
        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    # Display Page
    return render_template(
        'add_potty_log.html',
        form=form,
        child=child,
        daily_log=daily_log,
        selected_date=selected_date
    )

# Edit Potty Log
@app.route('/daily-log/<int:child_id>/potty/<int:log_id>/edit', methods=['GET', 'POST'])
def edit_potty_log(child_id, log_id):

     child = Child.query.get_or_404(child_id)

     potty_log = PottyLog.query.get_or_404(log_id)

     # Make sure this log belongs to this child
     daily_log = DailyLog.query.filter_by(
         id=potty_log.daily_log_id,
         child_id=child.id
     ).first_or_404()

     selected_date = daily_log.log_date

     form = PottyLogForm()

     # Load Existing Values
     if request.method == 'GET':

        form.potty_status.data = potty_log.potty_status
        form.potty_method.data = potty_log.potty_method
        form.potty_progress.data = potty_log.potty_progress
        form.notes.data = potty_log.notes or ''

        # Existing log time
        form.time_mode.data = 'manual'

        if potty_log.time:
            form.manual_time.data = potty_log.time.time()

     # Update
     if form.validate_on_submit():
         if form.time_mode.data == 'manual':

             if not form.manual_time.data:
                 form.manual_time.errors.append(
                     'Please enter the potty time.'
                 )

                 return render_template(
                     'edit_potty_log.html',
                     child=child,
                     daily_log=daily_log,
                     selected_date=selected_date,
                     potty_log=potty_log
                 )

             potty_log.time = datetime.combine(
                 selected_date,
                 form.manual_time.data
             )

         else:

             # Keep the existing time
             potty_log.time = potty_log.time

         potty_log.potty_status = form.potty_status.data
         potty_log.potty_method = form.potty_method.data
         potty_log.potty_progress = form.potty_progress.data
         potty_log.notes = form.notes.data 

         db.session.commit()

         flash(
             'Potty log updated successfully!',
             'success'
         )

         return redirect(
             url_for(
                 'child_daily_log',
                 child_id=child.id,
                 date=selected_date.strftime('%Y-%m-%d')
             )
         )

     return render_template(
         'edit_potty_log.html',
         form=form,
         child=child,
         daily_log=daily_log,
         selected_date=selected_date,
         potty_log=potty_log
     )
     
# Add Activity Log
@app.route('/daily-log/<int:child_id>/activity', methods=['GET','POST'])
def add_activity_log(child_id):

    child = Child.query.get_or_404(child_id)

    form = ActivityLogForm()

    # Selected Date
    date_string = request.args.get('date')

    if date_string:
        try:
            selected_date = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()

        except ValueError:
            selected_date = date.today()
    else:
        selected_date = date.today()

    # Save Activity Log
    if form.validate_on_submit():

        # Determine activity time
        if form.time_option.data == 'automatic':
            activity_time = datetime.now().time()

        else:
            activity_time = form.manual_time.data

        # Find daily log for selected date
        daily_log = DailyLog.query.filter_by(
            child_id=child.id,
            log_date=selected_date
        ).first()

        # Create daily log if it doesn't exist
        if not daily_log:
            daily_log = DailyLog(
                child_id=child.id,
                log_date=selected_date
            )

            db.session.add(daily_log)
            db.session.flush()

        # Convert activity values to readable labels
        activity_choices = dict(form.activity.choices)

        # Create one ActivityLog per selected activity
        for activity in form.activity.data:

            if activity == 'other':

                activity_name = (
                    form.other_activity.data or ''
                ).strip()

            else:
                activity_name = activity_choices.get(
                    activity,
                    activity
                )

            activity_log = ActivityLog(
                daily_log_id=daily_log.id,
                time=activity_time,
                activity=activity_name,
                notes=form.notes.data
            )

            db.session.add(activity_log)

        # Save everything
        db.session.commit()

        flash(
            'Activity log added successfully!',
            'success'
        )

        # Retun to selected day's log
        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    # Display form
    return render_template(
        'add_activity.html',
        child=child,
        form=form,
        selected_date=selected_date
    )

# Edit Activity Log
@app.route('/daily-log/<int:child_id>/activity/<int:log_id>/edit', methods=['GET', 'POST'])
def edit_activity_log(child_id, log_id):

    child = Child.query.get_or_404(child_id)
    activity_log = ActivityLog.query.get_or_404(log_id)

    # Make sure this activity log belongs to this child
    daily_log = DailyLog.query.filter_by(
        id=activity_log.daily_log_id,
        child_id=child.id
    ).first_or_404()

    selected_date = daily_log.log_date

    form = ActivityLogForm()

    # Load Existing Values
    if request.method == 'GET':

        # Find the saved activity in the form choices
        activity_choices = dict(form.activity.choices)

        matching_value = None

        for value, label in form.activity.choices:
            if label == activity_log.activity:
                matching_value = value
                break

        if matching_value:
            form.activity.data = [matching_value]

        else:
            # Saved activity was a custom "Other" activity
            form.activity.data = ['other']
            form.other_activity.data = activity_log.activity

        # Existing time
        form.time_option.data = 'manual'
        form.manual_time.data = activity_log.time

        # Existing notes
        form.notes.data = activity_log.notes or ''

    # Save Changes
    if form.validate_on_submit():

        # Determine activity name
        activity_choices = dict(form.activity.choices)

        selected_activity = form.activity.data[0]

        if selected_activity == 'other':

            activity_name = (
                form.other_activity.data or ''
            ).strip()

        else:

            activity_name = activity_choices.get(
                selected_activity,
                selected_activity
            )

        # Determine time
        if form.time_option.data == 'automatic':

            # Keep the originala time when editing
            activity_time = activity_log.time

        else:

            activity_time = form.manual_time.data 

        # Update existing activity log
        activity_log.activity = activity_name
        activity_log.time = activity_time
        activity_log.notes = form.notes.data 

        db.session.commit()

        flash(
            'Activity log updated successfully!',
            'success'
        )

        return redirect(
            url_for(
                'child_daily_log',
                child_id=child.id,
                date=selected_date.strftime('%Y-%m-%d')
            )
        )

    return render_template(
        'edit_activity.html',
        child=child,
        form=form,
        selected_date=selected_date,
        activity_log=activity_log
    )

# PDF
@app.route('/daily-log/<int:child_id>/pdf')
def daily_log_pdf(child_id):

    child = Child.query.get_or_404(child_id)

    date_string = request.args.get('date')

    if date_string:
        selected_date = datetime.strptime(
            date_string,
            '%Y-%m-%d'
        ).date()
    else:
        selected_date = date.today()

    daily_log = DailyLog.query.filter_by(
        child_id=child.id,
        log_date=selected_date
    ).first()

    if not daily_log:
        return "No daily log found for this date.", 404

    file_path = os.path.join(
        app.root_path,
        'daily_log_report.pdf'
    )

    create_daily_log_pdf(
        file_path,
        daily_log
    )

    return send_file(
        file_path,
        as_attachment=False,
        mimetype='application/pdf'
    )

# Email Daily Log
@app.route('/daily-log/<int:child_id>/email', methods=['GET', 'POST'])
def email_daily_log(child_id):

    child = Child.query.get_or_404(child_id)

    # Selected date
    date_string = request.args.get('date')

    if date_string:
        try:
            selected_date = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()

        except ValueError:
            selected_date = date.today()

    else:
        selected_date = date.today()

    # Find Daily Log
    daily_log = DailyLog.query.filter_by(
        child_id=child.id,
        log_date=selected_date
    ).first()

    if not daily_log:
        return "No daily log found for this date.", 404

    # Get parents who have an email address
    parent_emails = [
        parent
        for parent in child.parents
        if parent.email
    ]

    # Send Email
    if request.method == 'POST':

        selected_emails = request.form.getlist('emails')

        if not selected_emails:
            flash(
                "Please select at least one parent or guardian.",
                'warning'
            )

            return render_template(
                'email_daily_log.html',
                child=child,
                selected_date=selected_date,
                parent_emails=parent_emails,
                selected_emails=[]
            )

        file_path = None

        try:
            # ----------------------------------------
            # Create PDF
            # ----------------------------------------

            file_path = os.path.join(
                app.root_path,
                f'daily_log_{child.id}_{selected_date}.pdf'
            )

            create_daily_log_pdf(
                file_path,
                daily_log
            )

            # ----------------------------------------
            # Read PDF
            # ----------------------------------------

            with open(file_path, 'rb') as pdf_file:
                pdf_data = pdf_file.read()

            # ----------------------------------------
            # Create Resend Email
            # ----------------------------------------

            params = {
                "from": "onboarding@resend.dev",
                "to": selected_emails,
                "subject": (
                    f'Daily Log - '
                    f'{child.first_name} {child.last_name}'
                ),
                "html": f"""
                    <p>Hello,</p>

                    <p>
                        Please find attached the daily log for
                        <strong>
                            {child.first_name} {child.last_name}
                        </strong>
                        for
                        {selected_date.strftime('%B %d, %Y')}.
                    </p>

                    <p>
                        Thank you,<br>
                        Little Ones Too Daycare
                    </p>
                """,
                "attachments": [
                    {
                        "filename": "daily_log.pdf",
                        "content": pdf_data
                    }
                ]
            }

            # ----------------------------------------
            # Send Email through Resend
            # ----------------------------------------

            email = resend.Emails.send(params)

            app.logger.info(
                "Daily log email sent successfully: %s",
                email
            )

            flash(
                'Daily log sent successfully!',
                'success'
            )

            return redirect(
                url_for(
                    'child_daily_log',
                    child_id=child.id,
                    date=selected_date.strftime('%Y-%m-%d')
                )
            )

        except Exception as e:

            app.logger.exception(
                "Error sending daily log email through Resend: %s",
                e
            )

            flash(
                'Unable to send the daily log email. Please try again.',
                'danger'
            )

            return render_template(
                'email_daily_log.html',
                child=child,
                selected_date=selected_date,
                parent_emails=parent_emails,
                selected_emails=selected_emails
            )

        finally:

            # ----------------------------------------
            # Delete temporary PDF
            # ----------------------------------------

            if file_path and os.path.exists(file_path):

                try:
                    os.remove(file_path)

                except OSError:
                    pass

    # Display Email Page
    return render_template(
        'email_daily_log.html',
        child=child,
        selected_date=selected_date,
        parent_emails=parent_emails,
        selected_emails=[]
    )

# WhatsApp Route
@app.route('/daily-log/<int:child_id>/whatsapp')
def whatsapp_daily_log(child_id):

    child = Child.query.get_or_404(child_id)

    date_string = request.args.get('date')

    if date_string:
        selected_date = datetime.strptime(
            date_string,
            '%Y-%m-%d'
        ).date()
    else:
        selected_date = date.today()

    daily_log = DailyLog.query.filter_by(
        child_id=child.id,
        log_date=selected_date
    ).first()

    if not daily_log:
        return "No daily log found for this date.", 404

    return render_template(
        'whatsapp_daily_log.html',
        child=child,
        selected_date=selected_date
    )

# Calendar
@app.route('/calendar')
def calendar_view():

    today = date.today()

    # Selected Month
    year = request.args.get('year', today.year, type=int)
    month = request.args.get('month', today.month, type=int)

    # Keep month within valid range
    if month < 1:
        month = 12
        year -= 1

    elif month > 12:
        month = 1
        year += 1

    # Calendar grid
    cal = calendar.Calendar(firstweekday=6)

    month_days = cal.monthdatescalendar(year, month)

    # Events for selected month
    first_day = date(year, month, 1)

    if month == 12:
        next_month = date(year + 1, 1, 1)

    else:
        next_month = date(year, month + 1, 1)

    last_day = next_month.fromordinal(
        next_month.toordinal() - 1
    )

    events = Event.query.filter(
        Event.event_date >= first_day,
        Event.event_date <= last_day
    ).order_by(
        Event.event_date,
        Event.start_time
    ).all()

    # Group events by date
    events_by_date = {}

    for event in events:

        if event.event_date not in events_by_date:
            events_by_date[event.event_date] = []

        events_by_date[event.event_date].append(event)

    # Previous / next month

    if month == 1:
        previous_month = 12
        previous_year = year - 1

    else:
        previous_month = month - 1
        previous_year = year 

    if month == 12:
        next_month_number = 1
        next_year = year + 1

    else:
        next_month_number = month + 1
        next_year = year 

    # Upcoming events
    upcoming_events = Event.query.filter(
        Event.event_date >= today
    ).order_by(
        Event.event_date,
        Event.start_time 
    ).limit(5).all()

    return render_template(
        'calendar.html',
        month_days = month_days,
        events_by_date = events_by_date,
        current_month = date(year, month, 1),
        today=today,
        previous_month=previous_month,
        previous_year=previous_year,
        next_month=next_month_number,
        next_year=next_year,
        upcoming_events=upcoming_events
    )

# Add Event
@app.route('/calendar/add', methods=['GET', 'POST'])
def add_event():

    form = EventForm()

    # Allow clicking a specific calendar date
    date_string = request.args.get('date')

    if request.method == 'GET' and date_string:
        try:
            form.event_date.data = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()

        except ValueError:
            pass

    if form.validate_on_submit():

        event = Event(
            title=form.title.data,
            event_date=form.event_date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            event_type=form.event_type.data,
            class_name=form.class_name.data,
            description=form.description.data
        )

        db.session.add(event)
        db.session.commit()

        flash('Event added successfully', 'success')

        return redirect(url_for(
            'calendar_view',
            year=event.event_date.year,
            month=event.event_date.month
        ))

    return render_template(
        'add_event.html',
        form=form
    )

# Edit Event
@app.route('/calendar/edit/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):

    event = Event.query.get_or_404(event_id)

    form = EventForm(obj=event)

    if form.validate_on_submit():

        event.title = form.title.data
        event.event_date = form.event_date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.event_type = form.event_type.data
        event.class_name = form.class_name.data
        event.description = form.description.data 

        db.session.commit()

        flash('Event updated successfully!', 'success')

        return redirect(url_for(
            'calendar_view',
            year=event.event_date.year,
            month=event.event_date.month
        ))

    return render_template(
        'edit_event.html',
        form=form,
        event=event
    )

# Deleve Event
@app.route('/calendar/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):

    event = Event.query.get_or_404(event_id)

    event_month = event.event_date.month
    event_year = event.event_date.year

    db.session.delete(event)
    db.session.commit()

    flash('Event deleted successfully!', 'success')

    return redirect(url_for(
        'calendar_view',
        year=event_year,
        month=event_month
    ))

# Reports
@app.route('/reports')
def reports():
    return render_template('reports/reports.html')

# Student Directory
@app.route('/reports/students')
def student_directory_report():

    children = Child.query.order_by(
        Child.last_name.asc(),
        Child.first_name.asc()
    ).all()

    total_students = len(children)
    today = date.today()

    return render_template(
        'reports/student_directory.html',
        children=children,
        total_students=total_students,
        today=today
    )

# Student Directory PDF
@app.route('/reports/students/pdf')
def student_directory_pdf():

    children = Child.query.order_by(
        Child.last_name.asc(),
        Child.first_name.asc()
    ).all()

    file_path = os.path.join(
        app.config.get(
            'UPLOAD_FOLDER',
            'static/uploads'
        ),
        'student_directory_report.pdf'
    )

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    create_student_directory_pdf(
        file_path,
        children
    )

    return send_file(
        file_path,
        as_attachment=False,
        mimetype='application/pdf'
    )

# Students by Class
@app.route('/reports/students-by-class')
def students_by_class_report():

    children = Child.query.order_by(
        Child.class_name.asc(),
        Child.last_name.asc(),
        Child.first_name.asc()
    ).all()

    classes = {}
    today = date.today()

    for child in children:
        class_name = child.class_name or 'Unassigned'

        if class_name not in classes:
            classes[class_name] = []

        classes[class_name].append(child)

    return render_template(
        'reports/students_by_class.html',
        classes=classes,
        total_students=len(children),
        today=today
    )

# Students by Class PDF
@app.route('/reports/students-by-class/pdf')
def students_by_class_pdf():

    children = Child.query.order_by(
        Child.class_name.asc(),
        Child.last_name.asc(),
        Child.first_name.asc()
    ).all()

    classes = {}

    for child in children:

        class_name = child.class_name or 'Unassigned'

        if class_name not in classes:
            classes[class_name] = []

        classes[class_name].append(child)

    file_path = os.path.join(
        app.config.get(
            'UPLOAD_FOLDER',
            'static/uploads'
        ),
        'students_by_class_report.pdf'
    )

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    create_students_by_class_pdf(
        file_path,
        classes
    )

    return send_file(
        file_path,
        as_attachment=False,
        mimetype='application/pdf'
    )

# Enrollment Summary PDF
@app.route('/reports/enrollment-summary/pdf')
def enrollment_summary_pdf():

    children = Child.query.order_by(
        Child.enrolled_date.asc(),
        Child.last_name.asc(),
        Child.first_name.asc()
    ).all()

    # Total students
    total_students = len(children)

    # Gender summary
    male_count = sum(
        1 for child in children
        if child.gender == 'male'
    )

    female_count = sum(
        1 for child in children
        if child.gender == 'female'
    )

    # Class summary
    class_counts = {}

    for child in children:

        class_name = child.class_name or 'Unassigned'

        if class_name not in class_counts:
            class_counts[class_name] = 0

        class_counts[class_name] += 1

    # Program summary
    program_counts = {}

    for child in children:
        program = child.program_type or 'Unassigned'

        if program not in program_counts:
            program_counts[program] = 0

        program_counts[program] += 1

    # Enrollment year summary
    enrollment_years = {}

    for child in children:
        if child.enrolled_date:
            year = child.enrolled_date.year

            if year not in enrollment_years:
                enrollment_years[year] = 0

            enrollment_years[year] += 1

    enrollment_years = dict(
        sorted(
            enrollment_years.items(),
            reverse=True 
        )
    )

    # PDF file
    file_path = os.path.join(
        app.config.get(
            'UPLOAD_FOLDER',
            'static/uploads'
        ),
        'enrollment_summary_report.pdf'
    )

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    create_enrollment_summary_pdf(
        file_path,
        total_students,
        male_count,
        female_count,
        class_counts,
        program_counts,
        enrollment_years
    )

    return send_file(
        file_path,
        as_attachment=False,
        mimetype='application/pdf'
    )

# Student Directory Preview
@app.route('/reports/students/preview')
def student_directory_preview():

    return render_template(
        'reports/pdf_preview.html',
        title='Student Directory',
        pdf_url=url_for('student_directory_pdf')
    )

# Student By Class Preview
@app.route('/reports/students-by-class/preview')
def students_by_class_preview():

    return render_template(
        'reports/pdf_preview.html',
        title='Students by Class',
        pdf_url=url_for('students_by_class_pdf')
    )

# Enrollment Summary
@app.route('/reports/enrollment-summary/preview')
def enrollment_summary_preview():

    return render_template(
        'reports/pdf_preview.html',
        title='Enrollment Summary',
        pdf_url=url_for('enrollment_summary_pdf')
    )

# Daily Log Report Selector
@app.route('/reports/daily-log')
def daily_log_report():

    # Selected date
    date_string = request.args.get('date')

    if date_string:
        try:
            selected_date = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()

        except ValueError:
            selected_date = date.today()

    else:
        selected_date = date.today()

    # Selected class
    selected_class = request.args.get(
        'class_name',
        'all'
    )

    # Class choices
    classes = [
        'Infant',
        'Toddler',
        'Pre-K',
        'After School'
    ]

    # PDF URL
    pdf_url = url_for(
        'daily_log_report_pdf',
        date=selected_date.strftime('%Y-%m-%d'),
        class_name=selected_class
    )

    return render_template(
        'reports/daily_log_report.html',
        selected_date=selected_date,
        selected_class=selected_class,
        classes=classes,
        pdf_url=pdf_url
    )

# Daily Log Report PDF
@app.route('/reports/daily-log/pdf')
def daily_log_report_pdf():

    date_string = request.args.get('date')

    if date_string:

        try:
            selected_date = datetime.strptime(
                date_string,
                '%Y-%m-%d'
            ).date()

        except ValueError:
            selected_date = date.today()

    else:
        selected_date = date.today()

    # Selected class
    selected_class = request.args.get(
        'class_name',
        'all'
    )

    # Get children
    children_query = Child.query

    # Apply class filter
    if selected_class != 'all':
        children_query = children_query.filter(
            Child.class_name == selected_class
        )

    children = children_query.order_by(
        Child.last_name.asc(),
        Child.first_name.asc()
    ).all()

    # Get daily logs for selected dates
    logs = DailyLog.query.filter_by(
        log_date = selected_date
    ).all()

    # Maps logs by child
    daily_logs = {
        log.child_id: log 
        for log in logs
    }

    # PDF path
    file_path = os.path.join(
        app.config.get(
            'UPLOAD_FOLDER',
            'static/uploads'
        ),
        'daily_log_report.pdf'
    )

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    # Create PDF
    create_daily_log_report_pdf(
        file_path,
        children,
        daily_logs,
        selected_date
    )

    return send_file(
        file_path,
        as_attachment=False,
        mimetype='application/pdf'
    )

# Birthday PDF
@app.route('/reports/birthdays/pdf')
def birthday_report_pdf():

    month_string = request.args.get(
        'month',
        str(date.today().month)
    )

    try:
        selected_month = int(month_string)

        if selected_month < 1 or selected_month > 12:
            selected_month = date.today().month

    except ValueError:
        selected_month = date.today().month

    month_name = date(
        2000,
        selected_month,
        1
    ).strftime('%B')

    # Get children with birthdays

    children = [
        child
        for child in Child.query.order_by(
            Child.last_name.asc(),
            Child.first_name.asc()
        ).all()
        if child.date_of_birth
        and child.date_of_birth.month == selected_month
    ]

    # Sort by birthday
    children.sort(
        key=lambda child: (
            child.date_of_birth.day,
            child.last_name.lower(),
            child.first_name.lower()
        )
    )

    # Create PDF
    file_path = os.path.join(
        app.config.get(
            'UPLOAD_FOLDER',
            'static/uploads'
        ),
        'birthday_report.pdf'
    )

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    create_birthday_report_pdf(
        file_path,
        children,
        selected_month,
        month_name
    )

    return send_file(
        file_path,
        as_attachment=False,
        mimetype='application/pdf'
    )

# Birthday PDF Preview
@app.route('/reports/birthdays/preview')
def birthday_report_preview():

    month_string = request.args.get(
        'month',
        str(date.today().month)
    )

    try:
        selected_month = int(month_string)

        if selected_month < 1 or selected_month > 12:
            selected_month = date.today().month

    except ValueError:
        selected_month = date.today().month

    month_name = date(
        2000,
        selected_month,
        1
    ).strftime('%B')

    pdf_url = url_for(
        'birthday_report_pdf',
        month=selected_month
    )

    return render_template(
        'reports/birthday_report.html',
        selected_month=selected_month,
        month_name=month_name,
        pdf_url=pdf_url
    )

# Parent Contact PDF Preview
@app.route('/reports/parent-contacts/pdf')
def parent_contact_report_pdf():

    student_id = request.args.get('student_id', 'all')

    children_query = Child.query

    if student_id != 'all':
        try:
            student_id = int(student_id)

            children_query = children_query.filter(
                Child.id == student_id 
            )
        except ValueError:
            student_id = 'all'

    children = children_query.order_by(
        Child.last_name.asc(),
        Child.first_name.asc()
    ).all()

    file_path = os.path.join(
        app.config.get(
            'UPLOAD_FOLDER',
            'static/uploads'
        ),
        'parent_contact_report.pdf'
    )

    os.makedirs(
        os.path.dirname(file_path),
        exist_ok=True
    )

    create_parent_contact_report_pdf(
        file_path,
        children
    )

    return send_file(
        file_path,
        as_attachment=False,
        mimetype='application/pdf'
    )

# Parent Contact PDF
@app.route('/reporst/parent-contacts/preview')
def parent_contact_report_preview():

    student_id = request.args.get(
        'student_id',
        'all'
    )

    children = Child.query.order_by(
        Child.last_name.asc(),
        Child.first_name.asc()
    ).all()

    pdf_url = url_for(
        'parent_contact_report_pdf',
        student_id=student_id 
    )

    return render_template(
        'reports/parent_contact_report.html',
        children=children,
        selected_student=student_id,
        pdf_url=pdf_url
    )




# App Run
if __name__ == '__main__':
    app.run(debug=True)

