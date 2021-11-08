import json
from flask import Blueprint
from flask_cors import cross_origin

profile_bp = Blueprint('profile', __name__, url_prefix='/user')

@profile_bp.route('/profile')
def profile():
    return 'retrieve profile from db here'