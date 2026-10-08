from app import app
from extensions import db
from models import (
    Child,
    Parent,
    AuthorizedPickup,
    DailyLog,
    DailyHealthCheck,
    MealLog,
    BottleLog,
    NapLog,
    DiaperLog,
    PottyLog,
    ActivityLog,
    Event
)

from datetime import date, time, datetime, timedelta


with app.app_context():

    # --------------------------------------------------
    # SAFETY CHECK
    # --------------------------------------------------

    existing_demo = Child.query.filter_by(
        first_name="Emma",
        last_name="Johnson"
    ).first()

    if existing_demo:
        print("Demo data already exists.")
        print("No changes were made.")
        exit()

    print("Adding Little Ones demo data...")

    # --------------------------------------------------
    # DATES
    # --------------------------------------------------

    today = date.today()
    yesterday = today - timedelta(days=1)
    two_days_ago = today - timedelta(days=2)


    # --------------------------------------------------
    # CHILD 1 - INFANT
    # --------------------------------------------------

    emma = Child(
        first_name="Emma",
        last_name="Johnson",
        date_of_birth=date(2026, 1, 15),
        gender="Female",

        street="123 Palm Street",
        city="Hagatna",
        state="GU",
        zipcode="96910",

        class_name="Infant",
        program_type="Full Day",
        days_attending="Monday, Tuesday, Wednesday, Thursday, Friday",
        enrolled_date=date(2026, 8, 1),
        start_date=date(2026, 8, 3),

        allergies="None",
        medical_notes="No known medical concerns.",
        notes="Enjoys music and sensory activities.",

        photo=None
    )

    db.session.add(emma)
    db.session.flush()


    emma_parent = Parent(
        child_id=emma.id,
        role="Mother",
        full_name="Sarah Johnson",
        occupation="Teacher",
        phone_number="(671) 555-0101",
        email="sarah.johnson@example.com"
    )

    emma_parent2 = Parent(
        child_id=emma.id,
        role="Father",
        full_name="David Johnson",
        occupation="Engineer",
        phone_number="(671) 555-0102",
        email="david.johnson@example.com"
    )

    emma_pickup = AuthorizedPickup(
        child_id=emma.id,
        full_name="Linda Johnson",
        relationship="Grandmother",
        phone="(671) 555-0103"
    )

    db.session.add_all([
        emma_parent,
        emma_parent2,
        emma_pickup
    ])


    # --------------------------------------------------
    # CHILD 2 - INFANT
    # --------------------------------------------------

    liam = Child(
        first_name="Liam",
        last_name="Williams",
        date_of_birth=date(2025, 12, 2),
        gender="Male",

        street="45 Marine Drive",
        city="Tamuning",
        state="GU",
        zipcode="96913",

        class_name="Infant",
        program_type="Full Day",
        days_attending="Monday, Tuesday, Wednesday, Thursday, Friday",
        enrolled_date=date(2026, 7, 15),
        start_date=date(2026, 7, 20),

        allergies="None",
        medical_notes="No known medical concerns.",
        notes="Likes books and singing.",

        photo=None
    )

    db.session.add(liam)
    db.session.flush()

    liam_parent = Parent(
        child_id=liam.id,
        role="Mother",
        full_name="Jessica Williams",
        occupation="Nurse",
        phone_number="(671) 555-0111",
        email="jessica.williams@example.com"
    )

    liam_pickup = AuthorizedPickup(
        child_id=liam.id,
        full_name="Robert Williams",
        relationship="Grandfather",
        phone="(671) 555-0112"
    )

    db.session.add_all([
        liam_parent,
        liam_pickup
    ])


    # --------------------------------------------------
    # CHILD 3 - TODDLER
    # --------------------------------------------------

    sophia = Child(
        first_name="Sophia",
        last_name="Brown",
        date_of_birth=date(2024, 2, 10),
        gender="Female",

        street="78 Sunrise Avenue",
        city="Dededo",
        state="GU",
        zipcode="96929",

        class_name="Toddler",
        program_type="Full Day",
        days_attending="Monday, Tuesday, Wednesday, Thursday, Friday",
        enrolled_date=date(2026, 6, 1),
        start_date=date(2026, 6, 8),

        allergies="Peanuts",
        medical_notes="Avoid all foods containing peanuts.",
        notes="Currently practicing independent hand washing.",

        photo=None
    )

    db.session.add(sophia)
    db.session.flush()

    sophia_parent = Parent(
        child_id=sophia.id,
        role="Mother",
        full_name="Maria Brown",
        occupation="Accountant",
        phone_number="(671) 555-0121",
        email="maria.brown@example.com"
    )

    sophia_parent2 = Parent(
        child_id=sophia.id,
        role="Father",
        full_name="James Brown",
        occupation="Electrician",
        phone_number="(671) 555-0122",
        email="james.brown@example.com"
    )

    sophia_pickup = AuthorizedPickup(
        child_id=sophia.id,
        full_name="Karen Brown",
        relationship="Aunt",
        phone="(671) 555-0123"
    )

    db.session.add_all([
        sophia_parent,
        sophia_parent2,
        sophia_pickup
    ])


    # --------------------------------------------------
    # CHILD 4 - TODDLER
    # --------------------------------------------------

    noah = Child(
        first_name="Noah",
        last_name="Davis",
        date_of_birth=date(2023, 11, 5),
        gender="Male",

        street="19 Coral Road",
        city="Mangilao",
        state="GU",
        zipcode="96913",

        class_name="Toddler",
        program_type="Full Day",
        days_attending="Monday, Wednesday, Friday",
        enrolled_date=date(2026, 5, 1),
        start_date=date(2026, 5, 4),

        allergies="Dairy",
        medical_notes="Avoid milk-based products.",
        notes="Working on potty training.",

        photo=None
    )

    db.session.add(noah)
    db.session.flush()

    noah_parent = Parent(
        child_id=noah.id,
        role="Father",
        full_name="Daniel Davis",
        occupation="Pilot",
        phone_number="(671) 555-0131",
        email="daniel.davis@example.com"
    )

    noah_pickup = AuthorizedPickup(
        child_id=noah.id,
        full_name="Rachel Davis",
        relationship="Mother",
        phone="(671) 555-0132"
    )

    db.session.add_all([
        noah_parent,
        noah_pickup
    ])


    # --------------------------------------------------
    # CHILD 5 - PRE-K
    # --------------------------------------------------

    olivia = Child(
        first_name="Olivia",
        last_name="Garcia",
        date_of_birth=date(2022, 4, 18),
        gender="Female",

        street="56 Gardenia Lane",
        city="Yigo",
        state="GU",
        zipcode="96929",

        class_name="Pre-K",
        program_type="Full Day",
        days_attending="Monday, Tuesday, Wednesday, Thursday, Friday",
        enrolled_date=date(2026, 4, 1),
        start_date=date(2026, 4, 6),

        allergies="None",
        medical_notes="No known medical concerns.",
        notes="Enjoys art, puzzles, and story time.",

        photo=None
    )

    db.session.add(olivia)
    db.session.flush()

    olivia_parent = Parent(
        child_id=olivia.id,
        role="Mother",
        full_name="Ana Garcia",
        occupation="Business Owner",
        phone_number="(671) 555-0141",
        email="ana.garcia@example.com"
    )

    olivia_pickup = AuthorizedPickup(
        child_id=olivia.id,
        full_name="Carlos Garcia",
        relationship="Uncle",
        phone="(671) 555-0142"
    )

    db.session.add_all([
        olivia_parent,
        olivia_pickup
    ])


    # --------------------------------------------------
    # CHILD 6 - PRE-K
    # --------------------------------------------------

    ethan = Child(
        first_name="Ethan",
        last_name="Martinez",
        date_of_birth=date(2021, 9, 22),
        gender="Male",

        street="91 Hibiscus Street",
        city="Barrigada",
        state="GU",
        zipcode="96913",

        class_name="Pre-K",
        program_type="Full Day",
        days_attending="Monday, Tuesday, Wednesday, Thursday, Friday",
        enrolled_date=date(2026, 3, 1),
        start_date=date(2026, 3, 2),

        allergies="None",
        medical_notes="No known medical concerns.",
        notes="Enjoys building blocks and outdoor play.",

        photo=None
    )

    db.session.add(ethan)
    db.session.flush()

    ethan_parent = Parent(
        child_id=ethan.id,
        role="Father",
        full_name="Michael Martinez",
        occupation="Software Developer",
        phone_number="(671) 555-0151",
        email="michael.martinez@example.com"
    )

    ethan_parent2 = Parent(
        child_id=ethan.id,
        role="Mother",
        full_name="Laura Martinez",
        occupation="Designer",
        phone_number="(671) 555-0152",
        email="laura.martinez@example.com"
    )

    ethan_pickup = AuthorizedPickup(
        child_id=ethan.id,
        full_name="Robert Martinez",
        relationship="Grandfather",
        phone="(671) 555-0153"
    )

    db.session.add_all([
        ethan_parent,
        ethan_parent2,
        ethan_pickup
    ])


    # --------------------------------------------------
    # CHILD 7 - AFTER SCHOOL
    # --------------------------------------------------

    mason = Child(
        first_name="Mason",
        last_name="Lee",
        date_of_birth=date(2019, 8, 14),
        gender="Male",

        street="22 Coconut Avenue",
        city="Tamuning",
        state="GU",
        zipcode="96913",

        class_name="After School",
        program_type="After School",
        days_attending="Monday, Tuesday, Wednesday, Thursday, Friday",
        enrolled_date=date(2026, 1, 5),
        start_date=date(2026, 1, 5),

        allergies="None",
        medical_notes="No known medical concerns.",
        notes="Enjoys reading, science activities, and outdoor games.",

        photo=None
    )

    db.session.add(mason)
    db.session.flush()

    mason_parent = Parent(
        child_id=mason.id,
        role="Mother",
        full_name="Jennifer Lee",
        occupation="Office Manager",
        phone_number="(671) 555-0161",
        email="jennifer.lee@example.com"
    )

    mason_pickup = AuthorizedPickup(
        child_id=mason.id,
        full_name="Kevin Lee",
        relationship="Uncle",
        phone="(671) 555-0162"
    )

    db.session.add_all([
        mason_parent,
        mason_pickup
    ])


    # --------------------------------------------------
    # DAILY LOG HELPER
    # --------------------------------------------------

    def create_daily_log(
        child,
        log_date,
        arrival,
        departure,
        notes
    ):

        daily_log = DailyLog(
            child_id=child.id,
            log_date=log_date,
            arrival_time=arrival,
            departure_time=departure,
            notes=notes
        )

        db.session.add(daily_log)
        db.session.flush()

        return daily_log


    # --------------------------------------------------
    # EMMA DAILY LOG
    # --------------------------------------------------

    log = create_daily_log(
        emma,
        today,
        time(7, 45),
        time(16, 30),
        "Emma had a happy morning and participated in sensory play."
    )

    db.session.add(DailyHealthCheck(
        daily_log_id=log.id,
        temperature=98.2,
        symptoms="None",
        notes="Appeared healthy and comfortable."
    ))

    db.session.add(BottleLog(
        daily_log_id=log.id,
        time=time(8, 15),
        bottle_type="Formula",
        amount_offered=6,
        notes="Finished bottle."
    ))

    db.session.add(BottleLog(
        daily_log_id=log.id,
        time=time(12, 30),
        bottle_type="Formula",
        amount_offered=5,
        notes="Drank most of bottle."
    ))

    db.session.add(NapLog(
        daily_log_id=log.id,
        start_time=time(9, 30),
        end_time=time(10, 45),
        notes="Slept peacefully."
    ))

    db.session.add(NapLog(
        daily_log_id=log.id,
        start_time=time(13, 15),
        end_time=time(14, 30),
        notes="Afternoon nap."
    ))

    db.session.add(DiaperLog(
        daily_log_id=log.id,
        time=time(10, 55),
        diaper_type="Wet",
        diaper_desc="Wet",
        notes=None
    ))

    db.session.add(DiaperLog(
        daily_log_id=log.id,
        time=time(14, 45),
        diaper_type="BM",
        diaper_desc="BM",
        notes="Changed before afternoon activity."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(11, 15),
        activity="Sensory Play",
        notes="Explored soft sensory blocks."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(15, 15),
        activity="Story Time",
        notes="Enjoyed listening to a picture book."
    ))


    # --------------------------------------------------
    # SOPHIA DAILY LOG
    # --------------------------------------------------

    log = create_daily_log(
        sophia,
        today,
        time(8, 0),
        time(16, 45),
        "Sophia had a positive day and practiced hand washing."
    )

    db.session.add(DailyHealthCheck(
        daily_log_id=log.id,
        temperature=98.4,
        symptoms="None",
        notes="No concerns observed."
    ))

    db.session.add(MealLog(
        daily_log_id=log.id,
        meal_type="Breakfast",
        time=time(8, 30),
        food="Oatmeal and banana",
        amount="Most",
        notes="Ate well."
    ))

    db.session.add(MealLog(
        daily_log_id=log.id,
        meal_type="Lunch",
        time=time(11, 45),
        food="Chicken, rice and vegetables",
        amount="Most",
        notes="Ate most of lunch."
    ))

    db.session.add(NapLog(
        daily_log_id=log.id,
        start_time=time(12, 45),
        end_time=time(14, 15),
        notes="Slept well."
    ))

    db.session.add(DiaperLog(
        daily_log_id=log.id,
        time=time(10, 15),
        diaper_type="Wet",
        diaper_desc="Wet",
        notes=None
    ))

    db.session.add(PottyLog(
        daily_log_id=log.id,
        time=datetime.combine(today, time(10, 45)),
        potty_status="wet",
        potty_method="toilet",
        potty_progress="used_with_assistance",
        notes="Needed help getting settled."
    ))

    db.session.add(PottyLog(
        daily_log_id=log.id,
        time=datetime.combine(today, time(14, 30)),
        potty_status="bm",
        potty_method="toilet",
        potty_progress="used_independently",
        notes="Successful BM."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(9, 30),
        activity="Art",
        notes="Finger painting activity."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(15, 0),
        activity="Outdoor Play",
        notes="Played on the playground with classmates."
    ))


    # --------------------------------------------------
    # NOAH DAILY LOG
    # --------------------------------------------------

    log = create_daily_log(
        noah,
        yesterday,
        time(8, 10),
        time(16, 30),
        "Noah practiced potty training throughout the day."
    )

    db.session.add(DailyHealthCheck(
        daily_log_id=log.id,
        temperature=98.1,
        symptoms="None",
        notes="Happy and active."
    ))

    db.session.add(MealLog(
        daily_log_id=log.id,
        meal_type="Breakfast",
        time=time(8, 30),
        food="Toast and fruit",
        amount="All",
        notes="Good appetite."
    ))

    db.session.add(MealLog(
        daily_log_id=log.id,
        meal_type="Lunch",
        time=time(11, 45),
        food="Turkey sandwich and fruit",
        amount="Most",
        notes=None
    ))

    db.session.add(NapLog(
        daily_log_id=log.id,
        start_time=time(12, 30),
        end_time=time(13, 45),
        notes="Short nap."
    ))

    db.session.add(PottyLog(
        daily_log_id=log.id,
        time=datetime.combine(yesterday, time(10, 0)),
        potty_status="wet",
        potty_method="toilet",
        potty_progress="used_with_assistance",
        notes="Needed verbal reminders."
    ))

    db.session.add(PottyLog(
        daily_log_id=log.id,
        time=datetime.combine(yesterday, time(13, 55)),
        potty_status="bm",
        potty_method="training_potty",
        potty_progress="used_independently",
        notes="Successful BM."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(9, 30),
        activity="Building Blocks",
        notes="Built a tall block tower."
    ))


    # --------------------------------------------------
    # OLIVIA DAILY LOG
    # --------------------------------------------------

    log = create_daily_log(
        olivia,
        today,
        time(7, 50),
        time(16, 40),
        "Olivia participated in classroom activities and story time."
    )

    db.session.add(DailyHealthCheck(
        daily_log_id=log.id,
        temperature=98.3,
        symptoms="None",
        notes="No concerns observed."
    ))

    db.session.add(MealLog(
        daily_log_id=log.id,
        meal_type="Breakfast",
        time=time(8, 20),
        food="Cereal and fruit",
        amount="All",
        notes="Ate breakfast independently."
    ))

    db.session.add(MealLog(
        daily_log_id=log.id,
        meal_type="Lunch",
        time=time(11, 45),
        food="Pasta and vegetables",
        amount="Most",
        notes=None
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(9, 30),
        activity="Story Time",
        notes="Participated in group discussion."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(14, 30),
        activity="Puzzle Activity",
        notes="Completed a 12-piece puzzle."
    ))


    # --------------------------------------------------
    # ETHAN DAILY LOG
    # --------------------------------------------------

    log = create_daily_log(
        ethan,
        yesterday,
        time(7, 55),
        time(16, 35),
        "Ethan had a great day and enjoyed outdoor play."
    )

    db.session.add(DailyHealthCheck(
        daily_log_id=log.id,
        temperature=98.0,
        symptoms="None",
        notes="Appeared healthy."
    ))

    db.session.add(MealLog(
        daily_log_id=log.id,
        meal_type="Lunch",
        time=time(12, 0),
        food="Chicken, rice and vegetables",
        amount="All",
        notes="Good appetite."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(10, 0),
        activity="Building Blocks",
        notes="Worked on a group building project."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(15, 0),
        activity="Outdoor Play",
        notes="Played soccer with classmates."
    ))


    # --------------------------------------------------
    # MASON DAILY LOG
    # --------------------------------------------------

    log = create_daily_log(
        mason,
        today,
        time(14, 30),
        time(17, 30),
        "Mason arrived after school and completed homework."
    )

    db.session.add(DailyHealthCheck(
        daily_log_id=log.id,
        temperature=98.2,
        symptoms="None",
        notes="Healthy and active."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(15, 0),
        activity="Homework",
        notes="Completed reading assignment."
    ))

    db.session.add(ActivityLog(
        daily_log_id=log.id,
        time=time(16, 15),
        activity="Outdoor Games",
        notes="Played basketball with classmates."
    ))


    # --------------------------------------------------
    # CALENDAR EVENTS
    # --------------------------------------------------

    events = [
        Event(
            title="Parent-Teacher Conference",
            event_date=today + timedelta(days=4),
            start_time=time(9, 0),
            end_time=time(12, 0),
            event_type="Meeting",
            class_name=None,
            description="Scheduled parent-teacher conferences."
        ),

        Event(
            title="Fall Art Activity",
            event_date=today + timedelta(days=7),
            start_time=time(10, 0),
            end_time=time(11, 30),
            event_type="Activity",
            class_name="Pre-K",
            description="Fall-themed classroom art activity."
        ),

        Event(
            title="Halloween Celebration",
            event_date=date(today.year, 10, 30),
            start_time=time(10, 0),
            end_time=time(12, 0),
            event_type="Celebration",
            class_name=None,
            description="Classroom Halloween celebration."
        ),

        Event(
            title="Staff Meeting",
            event_date=today + timedelta(days=12),
            start_time=time(17, 30),
            end_time=time(18, 30),
            event_type="Staff",
            class_name=None,
            description="Monthly staff meeting."
        ),

        Event(
            title="Family Day",
            event_date=today + timedelta(days=20),
            start_time=time(10, 0),
            end_time=time(14, 0),
            event_type="Family",
            class_name=None,
            description="Family activity day at the daycare."
        )
    ]

    db.session.add_all(events)


    # --------------------------------------------------
    # SAVE EVERYTHING
    # --------------------------------------------------

    db.session.commit()

    print()
    print("==========================================")
    print("Little Ones demo data created successfully!")
    print("==========================================")
    print()
    print("Children added: 7")
    print("Parents and authorized pickups added.")
    print("Daily logs added.")
    print("Meals, bottles, naps, diapers added.")
    print("Potty logs added.")
    print("Activities and health checks added.")
    print("Calendar events added.")
    print()
    print("All parent emails use fictional example.com addresses.")
    print()