"""
Configuration settings for Red Bull Network Optimizer
"""

import os

class Config:
    """Base configuration class."""
    
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'red-bull-optimizer-secret-key-2024'
    DEBUG = True
    
    # Data paths
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    
    # Optimization settings
    OPTIMIZATION_TIME_LIMIT = 30  # seconds
    SOLVER = 'PULP_CBC_CMD'  # PuLP default solver
    
    # Network parameters
    UNMET_DEMAND_PENALTY = 5.0  # EUR per unit (reflects lost revenue + brand damage)
    
    # Business constants
    WORKING_DAYS_PER_YEAR = 250
    MONTHS_PER_YEAR = 12
