from flask_login import current_user
from flask import render_template

@auth.route('/dashboard')
@login_required
def dashboard():
    role = current_user.role

    if role == 'student':
        return render_template('dashboard_student.html', username=current_user.username)
    elif role == 'faculty':
        return render_template('dashboard_faculty.html', username=current_user.username)
    elif role == 'admin':
        return render_template('dashboard_admin.html', username=current_user.username)
    else:
        return "Unknown role", 403
