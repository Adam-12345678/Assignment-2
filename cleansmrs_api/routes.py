from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, SensorData
from sqlalchemy import func

bp = Blueprint('api', __name__)

@bp.route('/api/sensor-data', methods=['POST'])
def create_sensor_data():
    data = request.json

    # Validate the incoming data
    required_fields = ['date', 'time', 'time_zone_offset', 'coordinates', 
                       'temperature_water', 'temperature_air', 'humidity', 
                       'wind_speed', 'wind_direction', 'precipitation', 
                       'haze', 'becquerel']
    
    if not data or any(key not in data for key in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        # Combine date and time to create a full datetime
        timestamp = datetime.fromisoformat(f"{data['date']}T{data['time']} {data['time_zone_offset']}")
    except ValueError:
        return jsonify({'error': 'Invalid date/time format. Date should be YYYYMMDD and Time should be hh:mm.'}), 400

    # Create a new SensorData object
    new_data = SensorData(
        timestamp=timestamp,
        coordinates=data['coordinates'],
        temperature_water=data['temperature_water'],
        temperature_air=data['temperature_air'],
        humidity=data['humidity'],
        wind_speed=data['wind_speed'],
        wind_direction=data['wind_direction'],
        precipitation=data['precipitation'],
        haze=data['haze'],
        becquerel=data['becquerel'],
    )
    
    # Add the sensor data to the database
    try:
        db.session.add(new_data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Data added successfully.', 'date': new_data.timestamp.date().isoformat()}), 201

@bp.route('/api/sensor-data', methods=['GET'])
def get_sensor_data():
    data = SensorData.query.all()
    return jsonify([{
        'date': d.timestamp.date().isoformat(),
        'timestamp': d.timestamp.isoformat(),
        'coordinates': d.coordinates,
        'temperature_water': d.temperature_water,
        'temperature_air': d.temperature_air,
        'humidity': d.humidity,
        'wind_speed': d.wind_speed,
        'wind_direction': d.wind_direction,
        'precipitation': d.precipitation,
        'haze': d.haze,
        'becquerel': d.becquerel
    } for d in data]), 200

@bp.route('/api/sensor-data/<string:date>', methods=['GET'])
def get_sensor_data_by_date(date):
    try:
        query_date = datetime.strptime(date, '%Y%m%d').date()  # Only get the date
    except ValueError:
        return jsonify({'error': 'Invalid date format. Expected YYYYMMDD.'}), 400
        
    # Use func.DATE to filter the timestamp correctly
    data = SensorData.query.filter(func.DATE(SensorData.timestamp) == query_date).all()
    
    if not data:
        return jsonify({'error': 'No data found for the specified date'}), 404

    return jsonify([{
        'date': d.timestamp.date().isoformat(),
        'timestamp': d.timestamp.isoformat(),
        'coordinates': d.coordinates,
        'temperature_water': d.temperature_water,
        'temperature_air': d.temperature_air,
        'humidity': d.humidity,
        'wind_speed': d.wind_speed,
        'wind_direction': d.wind_direction,
        'precipitation': d.precipitation,
        'haze': d.haze,
        'becquerel': d.becquerel
    } for d in data]), 200

@bp.route('/api/sensor-data/<string:date>', methods=['DELETE'])
def delete_sensor_data(date):
    try:
        query_date = datetime.strptime(date, '%Y%m%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Expected YYYYMMDD.'}), 400
        
    
    records_to_delete = SensorData.query.filter(func.DATE(SensorData.timestamp) == query_date).all()
    
    if not records_to_delete:
        return jsonify({'error': 'No data found for the specified date to delete'}), 404

    try:
        for record in records_to_delete:
            db.session.delete(record)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
        
    return jsonify({'message': 'Data deleted successfully.'}), 200  

@bp.route('/api/sensor-data/<string:date_str>', methods=['PUT'])
def edit_sensor_data(date_str):
    data = request.json
    
    
    try:
        query_date = datetime.strptime(date_str, '%Y%m%d').date()  
    except ValueError:
        return jsonify({'error': 'Invalid date format. Expected YYYYMMDD.'}), 400
    
    sensor_data = SensorData.query.filter(func.DATE(SensorData.timestamp) == query_date).first()

    if not sensor_data:
        return jsonify({'error': 'Sensor data not found.'}), 404

    # Update fields if present in the request
    optional_fields = ['coordinates', 'temperature_water', 'temperature_air', 
                       'humidity', 'wind_speed', 'wind_direction', 
                       'precipitation', 'haze', 'becquerel']
    
    for field in optional_fields:
        if field in data:
            setattr(sensor_data, field, data[field])

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': 'Data updated successfully.', 'date': sensor_data.timestamp.date().isoformat()}), 200