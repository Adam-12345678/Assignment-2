# Import SQLAlchemy extension for Flask to handle database operations
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database object
db = SQLAlchemy()

class SensorData(db.Model):
    """
    Database model representing environmental sensor readings.
    Stores comprehensive environmental data collected from sensors.
    """
    # Primary key for uniquely identifying each sensor data record
    id = db.Column(db.Integer, primary_key=True)
    
    # Timestamp of when the sensor reading was taken
    # Marked as required (nullable=False) to ensure every record has a time
    timestamp = db.Column(db.DateTime, nullable=False)
    
    # Geographic coordinates where the sensor data was collected
    # Stored as a string to support various coordinate formats
    coordinates = db.Column(db.String, nullable=False)
    
    # Water temperature measurement (can be null if not measured)
    temperature_water = db.Column(db.Float, nullable=True)
    
    # Air temperature measurement (can be null if not measured)
    temperature_air = db.Column(db.Float, nullable=True)
    
    # Humidity percentage (can be null if not measured)
    humidity = db.Column(db.Float, nullable=True)
    
    # Wind speed measurement (can be null if not measured)
    wind_speed = db.Column(db.Float, nullable=True)
    
    # Wind direction in degrees (can be null if not measured)
    wind_direction = db.Column(db.Float, nullable=True)
    
    # Precipitation amount (can be null if not measured)
    precipitation = db.Column(db.Float, nullable=True)
    
    # Haze condition (stored as a string for descriptive readings)
    haze = db.Column(db.String, nullable=True)
    
    # Radiation level in becquerels (can be null if not measured)
    becquerel = db.Column(db.Float, nullable=True)
