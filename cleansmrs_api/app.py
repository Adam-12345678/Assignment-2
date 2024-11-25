from flask import Flask
from models import db
from routes import bp  # Import the routes from routes.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Update this in production

# Initialize the database
db.init_app(app)

with app.app_context():
    db.create_all()

# Register the Blueprint for API routes
app.register_blueprint(bp)

@app.route('/')
def index():
    return "Welcome to the CleanSMRS API! Use /api/sensor-data to interact with sensor data."

if __name__ == '__main__':
    app.run(debug=True)