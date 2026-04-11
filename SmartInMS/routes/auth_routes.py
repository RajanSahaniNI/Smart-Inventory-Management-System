from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import UserModel

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('product_bp.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = UserModel.get_user_by_username(username)
        
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('product_bp.index'))
        else:
            flash('Invalid username or password.', 'danger')
            
    return render_template('login.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect(url_for('product_bp.index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if UserModel.get_user_by_username(username):
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('auth_bp.signup'))
        
        hashed_password = generate_password_hash(password)
        if UserModel.create_user(username, hashed_password):
            flash('Account created successfully! Please log in.', 'success')
            return redirect(url_for('auth_bp.login'))
        else:
            flash('Error creating account. Please try again.', 'danger')

    return render_template('signup.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth_bp.login'))
