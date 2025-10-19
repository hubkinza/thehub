# Imports 
from flask import Flask, request, jsonify, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from datetime import datetime, timedelta
from functools import wraps
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

#  APP SETUP 

my_app = Flask(__name__) 

# Configuration settings - NOW READING FROM ENVIRONMENT VARIABLES!
my_app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'fallback-secret-key-change-me')
my_app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
my_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
my_app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

db_object = SQLAlchemy(my_app) 
my_bcrypt_tool = Bcrypt(my_app) 
CORS(my_app, supports_credentials=True) 



#   SERVE HTML PAGES  

@my_app.route('/')
def index():
    return render_template('index.html')

@my_app.route('/<path:path>')
def serve_page(path):
    if path.endswith('.html'):
        return render_template(path)
    return my_app.send_static_file(path)

#  RUN APP  

if __name__ == '__main__':
    with my_app.app_context():
        db_object.create_all()
    my_app.run(debug=True, port=5000)
