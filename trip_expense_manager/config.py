"""
config.py - Configuration Settings
==================================
This file contains all configuration variables for the application.
Keeping configurations separate makes the app easier to maintain.
"""

import os

class Config:
    """
    Configuration class containing all app settings.
    
    Attributes:
        SECRET_KEY: Used for session security and CSRF protection
        SQLALCHEMY_DATABASE_URI: Database connection string
        SQLALCHEMY_TRACK_MODIFICATIONS: Disable modification tracking for performance
    """
    
    # Secret key for session management and CSRF protection
    # In production, use environment variable: os.environ.get('SECRET_KEY')
    SECRET_KEY = 'your-secret-key-change-in-production'
    
    # SQLite database file location
    # SQLite is perfect for college projects - no separate server needed
    SQLALCHEMY_DATABASE_URI = 'sqlite:///trip_expenses.db'
    
    # Disable Flask-SQLAlchemy event system (saves memory)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
