from flask import Flask, request, Response
from dotenv import load_dotenv
import os
from config import FLASK_SECRET_KEY
from werkzeug.security import check_password_hash

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

USERNAME = os.getenv("AUTH_USERNAME")
HASHED_PASSWORD = os.getenv("AUTH_PASSWORD")
print(f"Username: {USERNAME}, Password Hash: {HASHED_PASSWORD}")

def check_auth(username, password):
    
    return username == USERNAME and check_password_hash(HASHED_PASSWORD, password)

def authenticate():
    return Response(
        'Authentication required.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

@app.before_request
def require_authentication():
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
