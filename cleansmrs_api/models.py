from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    coordinates = db.Column(db.String, nullable=False)
    temperature_water = db.Column(db.Float, nullable=True)
    temperature_air = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    wind_speed = db.Column(db.Float, nullable=True)
    wind_direction = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)
    haze = db.Column(db.String, nullable=True)
    becquerel = db.Column(db.Float, nullable=True)