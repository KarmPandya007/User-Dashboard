from flask import Blueprint, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from models import Person

users_bp = Blueprint('users', __name__)

# Web Routes
@users_bp.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    return redirect(url_for('users.login_page'))

@users_bp.route('/login', methods=['GET'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    return render_template('login.html')

@users_bp.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = Person.get_by_email(email)
    if user and user.check_password(password):
        login_user(user)
        flash('Logged in successfully!', 'success')
        return redirect(url_for('users.home'))
    else:
        flash('Invalid email or password', 'error')
        return redirect(url_for('users.login_page'))

@users_bp.route('/register', methods=['GET'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('users.home'))
    return render_template('register.html')

@users_bp.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    age = int(request.form.get('age'))
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash('Passwords do not match', 'error')
        return redirect(url_for('users.register_page'))

    if Person.get_by_email(email):
        flash('Email already registered', 'error')
        return redirect(url_for('users.register_page'))

    try:
        user = Person.create({
            'name': name,
            'age': age,
            'email': email,
            'password': password
        })
        login_user(user)
        flash('Account created successfully!', 'success')
        return redirect(url_for('users.home'))
    except Exception as e:
        flash('Error creating account', 'error')
        return redirect(url_for('users.register_page'))

@users_bp.route('/home')
@login_required
def home():
    return render_template('home.html')

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('users.login_page'))

# API Routes (existing)
@users_bp.route('/api/users', methods=['GET'])
@login_required
def get_users():
    users = Person.get_all()
    return jsonify(users)

@users_bp.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'age', 'email', 'password')):
        return jsonify({'error': 'Missing required fields'}), 400
    user = Person.create(data)
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 201

@users_bp.route('/api/users/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    user = Person.get_by_id(user_id)
    if user:
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age})
    return jsonify({'error': 'User not found'}), 404

@users_bp.route('/api/users/<user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    data = request.get_json()
    if Person.update(user_id, data):
        return jsonify({'message': 'User updated'})
    return jsonify({'error': 'User not found'}), 404

@users_bp.route('/api/users/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
    if Person.delete(user_id):
        return jsonify({'message': 'User deleted'})
    return jsonify({'error': 'User not found'}), 404

