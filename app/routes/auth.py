from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from ..models import User
from .. import db, login_manager

auth = Blueprint('auth', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth.route('/')
def home():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')

    user = User.query.filter_by(username=username, password=password, role=role).first()
    if user:
        login_user(user)
        return redirect(url_for('auth.dashboard'))
    else:
        flash("Invalid credentials!")
        return redirect(url_for('auth.home'))

@auth.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.home'))
