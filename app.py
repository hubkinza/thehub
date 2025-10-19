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

#   DATABASE MODELS   

class User(db_object.Model): 
    # The columns for the User table
    user_id = db_object.Column('id', db_object.Integer, primary_key=True) 
    username = db_object.Column(db_object.String(80), unique=True, nullable=False)
    user_email = db_object.Column('email', db_object.String(120), unique=True, nullable=False) 
    password_hash_stored = db_object.Column('password_hash', db_object.String(200), nullable=False)
    is_user_admin = db_object.Column('is_admin', db_object.Boolean, default=False)
    account_created_at = db_object.Column('created_at', db_object.DateTime, default=datetime.utcnow)

    # Relationships to other tables
    posts = db_object.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan')
    comments = db_object.relationship('Comment', backref='author', lazy=True, cascade='all, delete-orphan')
    likes = db_object.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')

    # function to turn the database object into a dictionary (for JSON)
    def to_dict(self):
        return {
            'id': self.user_id,
            'username': self.username,
            'email': self.user_email,
            'is_admin': self.is_user_admin,
            'created_at': self.account_created_at.strftime('%Y-%m-%d')
        }

class Post(db_object.Model):
    # Columns for the Post table
    post_id = db_object.Column('id', db_object.Integer, primary_key=True)
    post_title = db_object.Column('title', db_object.String(200), nullable=False)
    post_content = db_object.Column('content', db_object.Text, nullable=False)
    post_tags = db_object.Column('tags', db_object.String(200))
    author_id_fk = db_object.Column('author_id', db_object.Integer, db_object.ForeignKey('user.id'), nullable=False)
    post_created_at = db_object.Column('created_at', db_object.DateTime, default=datetime.utcnow)
    post_updated_at = db_object.Column('updated_at', db_object.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    comments = db_object.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan')
    likes = db_object.relationship('Like', backref='post', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        # Calculate tags list
        if self.post_tags:
            tag_list = self.post_tags.split(',')
        else:
            tag_list = []

        # Get the like and comment count
        how_many_likes = len(self.likes)
        how_many_comments = len(self.comments)

        return {
            'id': self.post_id,
            'title': self.post_title,
            'content': self.post_content,
            'tags': tag_list,
            'author': self.author.username,
            'author_id': self.author_id_fk,
            'created_at': self.post_created_at.strftime('%B %d, %Y'),
            'updated_at': self.post_updated_at.strftime('%B %d, %Y'),
            'like_count': how_many_likes,
            'comment_count': how_many_comments
        }

class Comment(db_object.Model):
    # Columns for the Comment table
    comment_id = db_object.Column('id', db_object.Integer, primary_key=True)
    comment_text = db_object.Column('content', db_object.Text, nullable=False)
    author_id_fk = db_object.Column('author_id', db_object.Integer, db_object.ForeignKey('user.id'), nullable=False)
    post_id_fk = db_object.Column('post_id', db_object.Integer, db_object.ForeignKey('post.id'), nullable=False)
    comment_created_at = db_object.Column('created_at', db_object.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.comment_id,
            'content': self.comment_text,
            'author': self.author.username,
            'author_id': self.author_id_fk,
            'created_at': self.comment_created_at.strftime('%B %d, %Y')
        }

class Like(db_object.Model):
    # Columns for the Like table
    like_id = db_object.Column('id', db_object.Integer, primary_key=True)
    user_id_fk = db_object.Column('user_id', db_object.Integer, db_object.ForeignKey('user.id'), nullable=False)
    post_id_fk = db_object.Column('post_id', db_object.Integer, db_object.ForeignKey('post.id'), nullable=False)
    like_created_at = db_object.Column('created_at', db_object.DateTime, default=datetime.utcnow)

    # Make sure a user can only like a post once
    __table_args__ = (db_object.UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),)



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
