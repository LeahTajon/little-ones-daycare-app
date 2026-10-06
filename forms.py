from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    IntegerField,
    DateField,
    RadioField,
    SelectField,
    SelectMultipleField,
    EmailField,
    TextAreaField,
    TimeField,
    FloatField,
    BooleanField,
    SubmitField 
)
from wtforms.validators import DataRequired, Optional, ValidationError
from flask_wtf.file import FileField, FileAllowed

class ChildForm(FlaskForm):

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])

    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])

    street=StringField('Street')
    city=StringField('City')
    state=StringField('State')
    zipcode=StringField('ZIP Code')

    
    program_type = RadioField(
        'Program Type',
        choices=[
            ('Full Day', 'Full Day'),
            ('Half Day - Morning', 'Half Day - Morning'),
            ('Half Day - Afternoon', 'Half Day - Afternoon'),
            ('After School', 'After School')
        ]
    )

    enrolled_date = DateField(
        'Enrolled Date', 
        validators=[DataRequired()])

    start_date = DateField(
        'Start Date',
        validators=[DataRequired()])

    days_attending = SelectMultipleField(
        'Days Attending',
        choices=[
            ('Monday', 'Monday'),
            ('Tuesday', 'Tuesday'),
            ('Wednesday', 'Wednesday'),
            ('Thursday', 'Thursday'),
            ('Friday', 'Friday')
        ],
        coerce=str,
        default=[]
    )

    # Father Information
    father_name = StringField('Father Name')
    father_occupation = StringField('Occupation')
    father_phone = StringField('Phone Number')
    father_email = EmailField('Email Address')

    # Mother Information
    mother_name = StringField('Mother Name')
    mother_occupation = StringField('Occupation')
    mother_phone = StringField('Phone Number')
    mother_email = StringField('Email Address')

    # Authorized Pickup 1
    pickup1_name = StringField('Pickup 1 Name')
    pickup1_relationship = StringField('Relationship')
    pickup1_phone = StringField('Phone Number')

    # Authorized Pickup 2
    pickup2_name = StringField('Pickup 2 Name')
    pickup2_relationship = StringField('Relationship')
    pickup2_phone = StringField('Phone Number')

    # Authorized Pickup 3
    pickup3_name = StringField('Pickup 3 Name')
    pickup3_relationship = StringField('Relationship')
    pickup3_phone = StringField('Phone Number')

    # Child Photo
    photo = FileField('Child Photo', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'webp'], 'Images only!')])

    # Allergies
    allergies = TextAreaField('Allergies')

    # Medical Notes
    medical_notes = TextAreaField('Medical Notes')

    # Notes
    notes = TextAreaField('Additional Notes')

    submit = SubmitField('Save')

class BottleLogForm(FlaskForm):

    bottle_type = RadioField(
        'Bottle Type',
        choices=[
            ('formula', 'Formula'),
            ('milk', 'Milk'),
            ('breast_milk', 'Breast Milk'),
            ('water', 'Water'),
            ('other', 'Other')
        ],
        validators=[DataRequired()]
    )

    other_bottle = StringField(
        'Other Bottle',
        validators=[Optional()]
    )

    time_option = RadioField(
        'Time',
        choices=[
            ('automatic', 'Automatic'),
            ('manual', 'Manual')
        ],
        default='automatic',
        validators=[DataRequired()]
    )

    manual_time = TimeField(
        'Manual Time',
        format='%H:%M',
        validators=[Optional()]
    )

    amount_offered = FloatField(
        'Amount Offered',
        validators=[Optional()]
    )

    notes = TextAreaField(
        'Notes',
        validators=[Optional()]
    )

    submit = SubmitField(
        'Save Bottle Log'
    )

    def validate(self, extra_validators=None):

        if not super().validate(
            extra_validators=extra_validators
        ):
            return False

        # Manual time requires a time
        if (
            self.time_option.data == 'manual'
            and not self.manual_time.data
        ):
            self.manual_time.errors.append(
                'Please enter the bottle time.'
            )
            return False

        # Other requires a description
        if (
            self.bottle_type.data == 'other'
            and not (self.other_bottle.data or '').strip()
        ):
            self.other_bottle.errors.append(
                'Please enter the bottle type.'
            )
            return False

        return True
    
class MealLogForm(FlaskForm):

    # Meal Type
    meal_type = RadioField(
        'Meal Type',
        choices=[
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('snack', 'Snack')
        ],
        validators=[]
    )

    # Food
    food = SelectMultipleField(
        'Food',
        choices=[
            ('rice', 'Rice'),
            ('pasta_noodles', 'Pasta / Noodles'),
            ('chicken_meat', 'Chicken / Meat'),
            ('egg', 'Eggs'),
            ('vegetables', 'Vegetables'),
            ('fruit', 'Fruit'),
            ('bread', 'Bread'),
            ('cheese_yogurt', 'Cheese / Yogurt'),
            ('crackers_cookies', 'Crackers / Cookies'),
            ('cereal', 'Cereal'),
            ('chips', 'Chips'),
            ('juice_water', 'Juice / Water')
        ],
        coerce=str,
        default=[],
        validators=[DataRequired()]
    )

    # Other Food
    other_food = StringField(
        'Other Food',
        validators=[Optional()]
    )

    # Amount
    amount = RadioField(
        'Amount',
        choices=[
            ('none', 'None'),
            ('some', 'Some'),
            ('most', 'Most'),
            ('all', 'All')
        ],
        validators=[]
    )

    # Time
    time_option = RadioField(
        'Time',
        choices=[
            ('automatic', 'Automatic'),
            ('manual', 'Manual')
        ],
        default='automatic',
        validators=[DataRequired()]
    )

    manual_time = TimeField(
        'Manual Time',
        format='%H:%M',
        validators=[Optional()]
    )

    # Notes
    notes = TextAreaField(
        'Notes',
        validators=[Optional()]
    )

    # Submit
    submit = SubmitField(
        'Save Meal'
    )

    def validate(self, extra_validators=None):

        # Run normal Flask-WTF validation first
        if not super().validate(
            extra_validators=extra_validators
        ):
            return False

        # Manual time requires time
        if (
            self.time_option.data == 'manual'
            and not self.manual_time.data
        ):
            self.manual_time.errors.append(
                'Please enter the meal time.'
            )

            return False

        return True

class NapLogForm(FlaskForm):

    time_mode = RadioField(
        'Time',
        choices=[
            ('automatic', 'Automatic'),
            ('manual', 'Manual')
        ],
        default='automatic'
    )

    # Used by the Add Nap page
    nap_time = TimeField( 
        'Time',
        validators=[Optional()],
        format='%H:%M'
    )

    # Used by the Edit Nap page
    start_time = TimeField(
        'Start Time',
        validators=[Optional()],
        format='%H:%M'
    )

    end_time = TimeField(
        'End Time',
        validators=[Optional()],
        format='%H:%M'
    )

    submit = SubmitField('Start Nap')


class DiaperLogForm(FlaskForm):

    # Diaper Type
    diaper_type = RadioField(
        'Diaper Type',
        choices=[
            ('wet', 'Wet'),
            ('dry', 'Dry'),
            ('bm', 'BM')
        ],
        validators=[DataRequired(message='Please select a diaper type.')]
    )

    # Description
    diaper_desc = StringField(
        'Description',
        validators=[
            Optional()
        ]
    )

    # Notes
    notes = TextAreaField(
        'Notes',
        validators=[Optional()]
    )

    # Time Mode
    time_mode = RadioField(
        'Time',
        choices=[
            ('automatic', 'Automatic'),
            ('manual', 'Manual')
        ],
        default='automatic',
        validators=[DataRequired()]
    )

    # Manual Time
    manual_time = TimeField(
        'Manual Time',
        format='%H:%M',
        validators=[Optional()]
    )

    # Submit 
    submit = SubmitField(
        'Save Diaper Log'
    )


class PottyLogForm(FlaskForm):

    potty_status = RadioField(
        'Potty Status',
        choices=[
            ('wet','Wet'),
            ('bm', 'BM'),
            ('wet_bm', 'Wet + BM'),
        ],
        validators=[DataRequired()]
    )

    potty_method = RadioField(
        'Potty Method',
        choices=[
            ('toilet', 'Toilet'),
            ('diaper', 'Diaper'),
            ('pull_up', 'Pull-Up'),
            ('training_potty', 'Potty Chair'),
        ],
        validators=[DataRequired()]
    )

    potty_progress = RadioField(
        'Potty Training Progress',
        choices=[
            ('independent', 'Used Independently'),
            ('assistance', 'Used With Assistance'),
            ('sat', 'Sat on Potty'),
            ('no_result', 'Tried - No Result'),
            ('refused', 'Refused'),
            ('accident', 'Had an Accident'),
        ],
        validators=[Optional()]
    )

    time_mode = RadioField(
        'Time',
        choices=[
            ('automatic', 'Automatic'),
            ('manual', 'Manual')
        ],
        default='automatic'
    )

    manual_time = TimeField(
        'Manual Time',
        validators=[Optional()]
    )

    notes = TextAreaField(
        'Notes',
        validators=[Optional()]
    )

    submit = SubmitField('Save Potty Log')

class ActivityLogForm(FlaskForm):

    activity =SelectMultipleField(
        'Activities',
        choices=[
            ('art', 'Arts and Crafts'),
            ('assembly','Assembly and Group Activities'),
            ('worksheets', 'Worksheets and Table Activities'),
            ('music', 'Music'),
            ('reading', 'Reading'),
            ('outdoor_play', 'Outdoor Play'),
            ('indoor_play', 'Indoor Play'), 
            ('sensory_play', 'Sensory Play'),
            ('gross_motor', 'Gross Motor'),
            ('fine_motor', 'Fine Motor'),
            ('free_play', 'Free Play'),           
            ('other', 'Other')  
        ],
        coerce=str,
        default=[],
        validators=[DataRequired()]
    )

    other_activity = StringField(
        'Other Activity',
        validators=[Optional()]
    )

    time_option = RadioField(
        'Time',
        choices=[
            ('automatic', 'Automatic'),
            ('manual', 'Manual')
        ],
        default='automatic',
        validators=[DataRequired()]
    )

    manual_time = TimeField(
        'Manual Time',
        format='%H:%M',
        validators=[Optional()]
    )

    notes = TextAreaField(
        'Notes',
        validators=[Optional()]
    )

    submit = SubmitField('Save Activity Log')

    def validate(self, extra_validators=None):
        # Run the normal Flask-WTF validation first
        if not super().validate(extra_validators=extra_validators):
            return False

        # Manual time is required when Manual is selected
        if self.time_option.data == 'manual' and not self.manual_time.data:
            self.manual_time.errors.append(
                'Please enter the activity time.'
            )
            return False

        # Other activity is required when Other is selected
        if (
            'other' in self.activity.data
            and not (self.other_activity.data or '').strip()
        ):
            self.other_activity.errors.append(
                'Please enter the activity'
            )
            return False

        return True

class EventForm(FlaskForm):

    title = StringField(
        'Event Name',
        validators=[DataRequired()]
    )

    event_date = DateField(
        'Date',
        validators=[DataRequired()],
        format='%Y-%m-%d'
    )

    start_time = TimeField(
        'Start Time',
        validators=[Optional()]
    )

    end_time = TimeField(
        'End Time',
        validators=[Optional()]
    )

    event_type = SelectField(
        'Event Type',
        choices=[
            ('celebration', 'Celebration'),
            ('shcool', 'School'),
            ('holiday', 'Holiday'),
            ('meeting', 'Meeting'),
            ('activity', 'Activity'),
            ('other', 'Other')
        ],
        validators=[Optional()]
    )

    class_name = SelectField(
        'Class',
        choices=[
            ('all', 'All Classes'),
            ('Infant', 'Infant'),
            ('Toddler', 'Toddler'),
            ('Preschool', 'Preschool'),
            ('Afterschool', 'Afterschool')
        ],
        validators=[Optional()]
    )

    description = TextAreaField(
        'Description',
        validators=[Optional()]
    )

    submit = SubmitField('Save Event')