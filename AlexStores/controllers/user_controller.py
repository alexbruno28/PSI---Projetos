from flask import Blueprint, render_template
from flask_login import login_required, current_user

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/profile')
@login_required
def profile():
    return render_template('users/profile.html', user=current_user)
