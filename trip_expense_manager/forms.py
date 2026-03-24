"""
forms.py - Form Definitions using Flask-WTF
==========================================
WTForms provides form validation and CSRF protection.
Each form class represents an HTML form with validation rules.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, 
    FloatField, DateField, SelectField, TextAreaField
)
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, 
    NumberRange, ValidationError, Optional
)
from models import User, EXPENSE_CATEGORIES, CURRENCIES, PAYMENT_METHODS


class RegistrationForm(FlaskForm):
    """
    User Registration Form
    
    Fields:
        username: 3-20 characters, unique
        email: Valid email format, unique
        password: Minimum 6 characters
        confirm_password: Must match password
    """
    
    username = StringField('Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, max=20, message='Username must be 3-20 characters')
    ])
    
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Please enter a valid email address')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Password is required'),
        Length(min=6, message='Password must be at least 6 characters')
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message='Please confirm your password'),
        EqualTo('password', message='Passwords must match')
    ])
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        """
        Custom validator to check if username already exists.
        WTForms automatically calls methods named validate_<fieldname>
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose another.')
    
    def validate_email(self, email):
        """Custom validator to check if email already exists."""
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please use another.')


class LoginForm(FlaskForm):
    """
    User Login Form
    
    Simple form with username and password fields.
    """
    
    username = StringField('Username', validators=[
        DataRequired(message='Please enter your username')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='Please enter your password')
    ])
    
    submit = SubmitField('Login')


class TripForm(FlaskForm):
    """
    Create/Edit Trip Form
    
    Collects all information needed to create a new trip.
    """
    
    name = StringField('Trip Name', validators=[
        DataRequired(message='Trip name is required'),
        Length(max=100, message='Trip name cannot exceed 100 characters')
    ])
    
    destination = StringField('Destination', validators=[
        DataRequired(message='Destination is required'),
        Length(max=100)
    ])
    
    start_date = DateField('Start Date', validators=[
        DataRequired(message='Start date is required')
    ])
    
    end_date = DateField('End Date', validators=[
        DataRequired(message='End date is required')
    ])
    
    # Create choices list for currency dropdown
    base_currency = SelectField('Base Currency', 
        choices=[(code, f"{code} - {info['name']}") for code, info in CURRENCIES.items()],
        default='INR'
    )
    
    budget = FloatField('Budget', validators=[
        Optional(),
        NumberRange(min=0, message='Budget cannot be negative')
    ])
    
    description = TextAreaField('Description', validators=[
        Optional(),
        Length(max=500)
    ])
    
    submit = SubmitField('Save Trip')
    
    def validate_end_date(self, end_date):
        """Ensure end date is not before start date."""
        if self.start_date.data and end_date.data:
            if end_date.data < self.start_date.data:
                raise ValidationError('End date cannot be before start date')


class ExpenseForm(FlaskForm):
    """
    Add/Edit Expense Form
    
    Collects expense details including currency conversion.
    """
    
    description = StringField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(max=200)
    ])
    
    category = SelectField('Category',
        choices=[(cat, cat) for cat in EXPENSE_CATEGORIES],
        validators=[DataRequired()]
    )
    
    amount = FloatField('Amount', validators=[
        DataRequired(message='Amount is required'),
        NumberRange(min=0.01, message='Amount must be greater than 0')
    ])
    
    currency = SelectField('Currency',
        choices=[(code, f"{code} ({info['symbol']})") for code, info in CURRENCIES.items()],
        default='INR'
    )
    
    date = DateField('Date', validators=[
        DataRequired(message='Date is required')
    ])
    
    location = StringField('Location', validators=[
        Optional(),
        Length(max=100)
    ])
    
    payment_method = SelectField('Payment Method',
        choices=[(method, method) for method in PAYMENT_METHODS],
        default='Cash'
    )
    
    notes = TextAreaField('Notes', validators=[
        Optional(),
        Length(max=300)
    ])
    
    submit = SubmitField('Save Expense')
