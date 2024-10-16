from flask import Flask
from dotenv import load_dotenv
import os
from config import FLASK_SECRET_KEY

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Import routes from routes.py
from routes import main_bp

# Register the routes
app.register_blueprint(main_bp)
print("FLASK SECRET KEY THAT WILL BE SET" + FLASK_SECRET_KEY)
app.secret_key = FLASK_SECRET_KEY

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
