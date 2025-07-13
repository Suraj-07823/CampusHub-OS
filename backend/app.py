from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from models.user import User
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

bcrypt = Bcrypt(app)
mongo = PyMongo(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    return User(user_data) if user_data else None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        role = request.form['role']

        if mongo.db.users.find_one({'email': email}):
            flash('User already exists.')
            return redirect(url_for('register'))

        mongo.db.users.insert_one({
            'email': email,
            'password': password,
            'role': role
        })
        flash('Registration successful. Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_input = request.form['password']
        user_data = mongo.db.users.find_one({'email': email})

        if user_data and bcrypt.check_password_hash(user_data['password'], password_input):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
