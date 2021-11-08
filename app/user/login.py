import json
from flask import Blueprint
from flask_cors import cross_origin

login_bp = Blueprint('login', __name__, url_prefix='/user')

#find existing user
@login_bp.route('/login')
def get_user():
    return 'retrieve existing user here'