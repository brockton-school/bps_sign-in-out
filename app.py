from flask import Flask, request, Response
from dotenv import load_dotenv
import os
from config import FLASK_SECRET_KEY, PATH_TO_USERS
from werkzeug.security import check_password_hash
from utils import load_users_from_csv
from db_init import init_db

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Import routes from routes.py
from routes import main_bp

# Register the routes
app.register_blueprint(main_bp)
print("FLASK SECRET KEY THAT WILL BE SET " + FLASK_SECRET_KEY)
app.secret_key = FLASK_SECRET_KEY

# Get SQL config
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
}

# Initialize DB
engine = init_db(DB_CONFIG)


USERS = load_users_from_csv(PATH_TO_USERS)

# Authentication function
def check_auth(username, password):
    hashed_password = USERS.get(username)
    if not hashed_password:
        return False
    return check_password_hash(hashed_password, password)


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
