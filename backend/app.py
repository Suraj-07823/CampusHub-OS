from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_pymongo import PyMongo
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models.user import User
from config import Config
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
mongo = PyMongo(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        reg_id = request.form['reg_id']
        password = request.form['password']
        role = request.form['role']
        existing_user = mongo.db.users.find_one({'reg_id': reg_id})
        if existing_user:
            flash("Registration ID already exists.")
            return redirect(url_for('register'))
        hash_pw = generate_password_hash(password)
        user_id = mongo.db.users.insert_one({
            'reg_id': reg_id,
            'password': hash_pw,
            'role': role
        }).inserted_id
        user = mongo.db.users.find_one({'_id': user_id})
        login_user(User(user))
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        reg_id = request.form['reg_id']
        password = request.form['password']
        user_data = mongo.db.users.find_one({'reg_id': reg_id})
        if user_data and check_password_hash(user_data['password'], password):
            login_user(User(user_data))
            return redirect(url_for('dashboard'))
        flash("Invalid credentials.")
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
