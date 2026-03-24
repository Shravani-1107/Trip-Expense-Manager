"""
models.py - Database Models
===========================
This file defines the structure of our database tables using SQLAlchemy ORM.
ORM (Object-Relational Mapping) allows us to work with databases using Python objects.
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize SQLAlchemy - this will be connected to Flask app later
db = SQLAlchemy()


class User(UserMixin, db.Model):
    """
    User Model - Stores user account information
    
    UserMixin provides default implementations for:
    - is_authenticated: Returns True if user is logged in
    - is_active: Returns True if account is active
    - is_anonymous: Returns False for regular users
    - get_id(): Returns unique identifier for the user
    
    Attributes:
        id: Primary key, auto-incremented
        username: Unique username for login
        email: User's email address
        password_hash: Encrypted password (never store plain passwords!)
        created_at: When the account was created
        trips: Relationship to Trip model (one user can have many trips)
    """
    
    __tablename__ = 'users'  # Table name in database
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship: One user can have many trips
    # backref creates a 'user' attribute on Trip objects
    trips = db.relationship('Trip', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """
        Hash and store the password securely.
        Never store plain text passwords!
        
        Args:
            password: Plain text password from user
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """
        Verify a password against the stored hash.
        
        Args:
            password: Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """String representation for debugging"""
        return f'<User {self.username}>'


class Trip(db.Model):
    """
    Trip Model - Stores trip information
    
    Each trip belongs to one user and can have multiple expenses.
    
    Attributes:
        id: Primary key
        name: Trip name (e.g., "Goa Vacation 2024")
        destination: Trip destination/location
        start_date: Trip start date
        end_date: Trip end date
        base_currency: Currency used for the trip (INR, USD, EUR, etc.)
        budget: Planned budget for the trip
        description: Optional trip description
        user_id: Foreign key linking to user
        expenses: Relationship to Expense model
    """
    
    __tablename__ = 'trips'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    base_currency = db.Column(db.String(3), default='INR')  # ISO currency code
    budget = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key - links this trip to a user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationship: One trip can have many expenses
    expenses = db.relationship('Expense', backref='trip', lazy=True, cascade='all, delete-orphan')
    
    @property
    def total_expenses(self):
        """
        Calculate total expenses for this trip.
        Property decorator allows us to access this like an attribute.
        
        Returns:
            float: Sum of all expense amounts
        """
        return sum(expense.amount_in_base_currency for expense in self.expenses)
    
    @property
    def remaining_budget(self):
        """
        Calculate remaining budget.
        
        Returns:
            float: Budget minus total expenses
        """
        return self.budget - self.total_expenses
    
    @property
    def duration_days(self):
        """
        Calculate trip duration in days.
        
        Returns:
            int: Number of days
        """
        return (self.end_date - self.start_date).days + 1
    
    def __repr__(self):
        return f'<Trip {self.name}>'


class Expense(db.Model):
    """
    Expense Model - Stores individual expense records
    
    Each expense belongs to one trip.
    
    Attributes:
        id: Primary key
        description: What the expense was for
        category: Type of expense (Food, Transport, etc.)
        amount: Expense amount
        currency: Currency of the expense
        exchange_rate: Exchange rate to base currency
        date: Date of expense
        day_of_trip: Which day of the trip (Day 1, Day 2, etc.)
        location: Where the expense occurred
        payment_method: How it was paid (Cash, Card, UPI)
        notes: Additional notes
        trip_id: Foreign key linking to trip
    """
    
    __tablename__ = 'expenses'
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='INR')
    exchange_rate = db.Column(db.Float, default=1.0)  # Rate to convert to base currency
    date = db.Column(db.Date, nullable=False)
    day_of_trip = db.Column(db.Integer)  # Day 1, Day 2, etc.
    location = db.Column(db.String(100))
    payment_method = db.Column(db.String(50), default='Cash')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key - links this expense to a trip
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    
    @property
    def amount_in_base_currency(self):
        """
        Convert expense amount to trip's base currency.
        
        Returns:
            float: Amount converted using exchange rate
        """
        return self.amount * self.exchange_rate
    
    def __repr__(self):
        return f'<Expense {self.description}: {self.amount} {self.currency}>'


# Expense categories - used for dropdown menus
EXPENSE_CATEGORIES = [
    'Food & Dining',
    'Transportation',
    'Accommodation',
    'Shopping',
    'Entertainment',
    'Sightseeing',
    'Communication',
    'Health & Medical',
    'Miscellaneous'
]

# Supported currencies with exchange rates (relative to INR)
# In a production app, you'd fetch these from an API
CURRENCIES = {
    'INR': {'name': 'Indian Rupee', 'symbol': '₹', 'rate_to_inr': 1.0},
    'USD': {'name': 'US Dollar', 'symbol': '$', 'rate_to_inr': 83.0},
    'EUR': {'name': 'Euro', 'symbol': '€', 'rate_to_inr': 90.0},
    'GBP': {'name': 'British Pound', 'symbol': '£', 'rate_to_inr': 105.0},
    'JPY': {'name': 'Japanese Yen', 'symbol': '¥', 'rate_to_inr': 0.55},
    'AUD': {'name': 'Australian Dollar', 'symbol': 'A$', 'rate_to_inr': 54.0},
    'SGD': {'name': 'Singapore Dollar', 'symbol': 'S$', 'rate_to_inr': 61.0},
    'THB': {'name': 'Thai Baht', 'symbol': '฿', 'rate_to_inr': 2.3},
    'AED': {'name': 'UAE Dirham', 'symbol': 'د.إ', 'rate_to_inr': 22.6}
}

# Payment methods
PAYMENT_METHODS = ['Cash', 'Credit Card', 'Debit Card', 'UPI', 'Net Banking', 'Traveler Cheque']
