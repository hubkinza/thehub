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


#   AUTH CHECK FUNCTIONS (DECORATORS)  

def login_required(function_to_decorate):
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            response_data = {'error': 'Authentication required'}
            return jsonify(response_data), 401
        return function_to_decorate(*args, **kwargs)
    return decorated_function

def admin_required(function_to_decorate):
    @wraps(function_to_decorate)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401

        current_user_id = session['user_id']
        user_info = User.query.get(current_user_id)

        if user_info is None or user_info.is_user_admin == False:
            return jsonify({'error': 'Admin privileges required'}), 403

        return function_to_decorate(*args, **kwargs)
    return decorated_function

#   AUTH ROUTES (Login/Logout/Register)  

@my_app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()

    if data is None or 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields in request'}), 400

    username_input = data['username']
    email_input = data['email']
    password_input = data['password']

    # Check if user already exists
    existing_user_by_email = User.query.filter_by(user_email=email_input).first()
    if existing_user_by_email is not None:
        return jsonify({'error': 'Email is already registered'}), 400

    existing_user_by_username = User.query.filter_by(username=username_input).first()
    if existing_user_by_username is not None:
        return jsonify({'error': 'Username is already taken by someone else'}), 400

    # Hash the password
    hashed_password_safe = my_bcrypt_tool.generate_password_hash(password_input).decode('utf-8')

    # Create new user
    new_user = User(
        username=username_input,
        user_email=email_input,
        password_hash_stored=hashed_password_safe,
        is_user_admin=False
    )

    db_object.session.add(new_user)
    db_object.session.commit()

    # Log the user in
    session['user_id'] = new_user.user_id
    session.permanent = True

    return jsonify({
        'message': 'Registration worked perfectly',
        'user': new_user.to_dict()
    }), 201

@my_app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if data is None or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'You must provide email AND password'}), 400

    login_email = data['email']
    login_password = data['password']

    the_user_we_are_looking_for = User.query.filter_by(user_email=login_email).first()

    if the_user_we_are_looking_for is None or not my_bcrypt_tool.check_password_hash(the_user_we_are_looking_for.password_hash_stored, login_password):
        return jsonify({'error': 'Invalid email or password. Please try again.'}), 401

    session['user_id'] = the_user_we_are_looking_for.user_id
    session.permanent = data.get('remember', False)

    return jsonify({
        'message': 'Login successful, welcome!',
        'user': the_user_we_are_looking_for.to_dict()
    }), 200

@my_app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'You have been logged out!'}), 200

@my_app.route('/api/current-user', methods=['GET'])
@login_required
def current_user():
    current_user_info = User.query.get(session['user_id'])
    return jsonify(current_user_info.to_dict()), 200
#   POST ROUTES  

@my_app.route('/api/posts', methods=['GET'])
def get_posts():
    page_number = request.args.get('page', 1, type=int)
    items_per_page = request.args.get('per_page', 10, type=int)
    search_term = request.args.get('search', '', type=str)

    the_query = Post.query

    if search_term != '':
        the_query = the_query.filter(
            (Post.post_title.contains(search_term)) |
            (Post.post_content.contains(search_term)) |
            (Post.post_tags.contains(search_term))
        )

    post_pages_object = the_query.order_by(Post.post_created_at.desc()).paginate(
        page=page_number, per_page=items_per_page, error_out=False
    )

    list_of_post_dictionaries = []
    for post_item in post_pages_object.items:
        list_of_post_dictionaries.append(post_item.to_dict())

    return jsonify({
        'posts': list_of_post_dictionaries,
        'total': post_pages_object.total,
        'page': post_pages_object.page,
        'pages': post_pages_object.pages
    }), 200

@my_app.route('/api/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    single_post = Post.query.get_or_404(post_id)
    return jsonify(single_post.to_dict()), 200

@my_app.route('/api/posts', methods=['POST'])
@login_required
def create_post():
    data = request.get_json()

    if data is None or 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Need a title and content for the post!'}), 400

    new_post = Post(
        post_title=data['title'],
        post_content=data['content'],
        post_tags=data.get('tags', ''),
        author_id_fk=session['user_id']
    )

    db_object.session.add(new_post)
    db_object.session.commit()

    return jsonify({
        'message': 'Post was created successfully!',
        'post': new_post.to_dict()
    }), 201

@my_app.route('/api/posts/<int:post_id>', methods=['PUT'])
@login_required
def update_post(post_id):
    post_to_edit = Post.query.get_or_404(post_id)

    if post_to_edit.author_id_fk != session['user_id']:
        return jsonify({'error': 'Sorry, you can only edit your own posts'}), 403

    data = request.get_json()

    if 'title' in data and data['title'] != '':
        post_to_edit.post_title = data['title']
    if 'content' in data and data['content'] != '':
        post_to_edit.post_content = data['content']
    if 'tags' in data:
        post_to_edit.post_tags = data['tags']

    post_to_edit.post_updated_at = datetime.utcnow()

    db_object.session.commit()

    return jsonify({
        'message': 'Post was updated!',
        'post': post_to_edit.to_dict()
    }), 200

@my_app.route('/api/posts/<int:post_id>', methods=['DELETE'])
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    current_user_object = User.query.get(session['user_id'])

    is_author = post_to_delete.author_id_fk == session['user_id']
    is_an_admin = current_user_object.is_user_admin

    if not is_author and not is_an_admin:
        return jsonify({'error': 'You do not have permission to delete this post'}), 403

    db_object.session.delete(post_to_delete)
    db_object.session.commit()

    return jsonify({'message': 'Post deleted successfully and permanently'}), 200
#   COMMENT ROUTES  

@my_app.route('/api/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    Post.query.get_or_404(post_id)
    comments_list = Comment.query.filter_by(post_id_fk=post_id).order_by(Comment.comment_created_at.desc()).all()
    comment_dict_list = [comment.to_dict() for comment in comments_list]
    return jsonify(comment_dict_list), 200

@my_app.route('/api/posts/<int:post_id>/comments', methods=['POST'])
@login_required
def create_comment(post_id):
    Post.query.get_or_404(post_id)
    data = request.get_json()

    if data is None or 'content' not in data or data['content'].strip() == '':
        return jsonify({'error': 'Comment content cannot be empty'}), 400

    new_comment = Comment(
        comment_text=data['content'],
        author_id_fk=session['user_id'],
        post_id_fk=post_id
    )

    db_object.session.add(new_comment)
    db_object.session.commit()

    return jsonify({
        'message': 'Comment was added!',
        'comment': new_comment.to_dict()
    }), 201

@my_app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment_to_delete = Comment.query.get_or_404(comment_id)
    current_user_object = User.query.get(session['user_id'])

    is_comment_author = comment_to_delete.author_id_fk == session['user_id']
    is_an_admin = current_user_object.is_user_admin

    if not is_comment_author and not is_an_admin:
        return jsonify({'error': 'You can only delete your own comments or be an admin'}), 403

    db_object.session.delete(comment_to_delete)
    db_object.session.commit()

    return jsonify({'message': 'Comment deleted'}), 200

#   LIKE ROUTES  

@my_app.route('/api/posts/<int:post_id>/like', methods=['POST'])
@login_required
def toggle_like(post_id):
    post_to_like = Post.query.get_or_404(post_id)
    current_user_id = session['user_id']

    existing_like = Like.query.filter_by(
        user_id_fk=current_user_id,
        post_id_fk=post_id
    ).first()

    if existing_like is not None:
        db_object.session.delete(existing_like)
        db_object.session.commit()
        new_like_count = len(post_to_like.likes)
        return jsonify({
            'message': 'Like was removed (unliked)',
            'liked': False,
            'like_count': new_like_count
        }), 200
    else:
        new_like = Like(user_id_fk=current_user_id, post_id_fk=post_id)
        db_object.session.add(new_like)
        db_object.session.commit()
        new_like_count = len(post_to_like.likes)
        return jsonify({
            'message': 'Post was liked!',
            'liked': True,
            'like_count': new_like_count
        }), 201
    
#   ADMIN ROUTES  

@my_app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    all_the_users = User.query.all()
    user_data_list = [user.to_dict() for user in all_the_users]
    return jsonify(user_data_list), 200

@my_app.route('/api/admin/posts', methods=['GET'])
@admin_required
def get_all_posts_admin():
    all_the_posts = Post.query.order_by(Post.post_created_at.desc()).all()
    post_data_list = [post.to_dict() for post in all_the_posts]
    return jsonify(post_data_list), 200

#   INITIALIZE DATABASE  

@my_app.route('/api/init-db', methods=['POST'])
def init_database():
    """Initialize database tables and create default admin user"""
    print("Trying to initialize the database...")
    try:
        db_object.create_all()

        # Get admin credentials from environment variables
        default_admin_email = os.getenv('ADMIN_EMAIL', 'admin@thehub.com')
        admin_default_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        
        admin_check = User.query.filter_by(user_email=default_admin_email).first()

        if admin_check is None:
            hashed_admin_password = my_bcrypt_tool.generate_password_hash(admin_default_password).decode('utf-8')

            new_admin_user = User(
                username='admin',
                user_email=default_admin_email,
                password_hash_stored=hashed_admin_password,
                is_user_admin=True
            )
            db_object.session.add(new_admin_user)
            db_object.session.commit()
            print("Default admin user created!")

        return jsonify({
            'message': 'Database tables are created and default admin is checked/created!',
            'admin_credentials': {
                'email': default_admin_email,
                'password': '***hidden***',
                'note': 'Check your .env file for credentials'
            }
        }), 200
    except Exception as e:
        print(f"Database initialization FAILED! Error: {e}")
        return jsonify({'error': 'Database setup failed: ' + str(e)}), 500


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
