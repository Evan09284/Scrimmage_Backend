import json
from flask import Blueprint
from flask_cors import cross_origin

auth_dash_bp = Blueprint('author_dashboard', __name__, url_prefix='/author')

@auth_dash_bp.route('/dashboard')
# @cross_origin(headers=['Content-Type', 'Authorization'])

def dash():
    return 'auth dash retreived and displayed here'