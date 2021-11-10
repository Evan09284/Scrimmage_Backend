import json
from flask import Blueprint
from flask_cors import cross_origin


home_bp = Blueprint('home', __name__, url_prefix='/')


@home_bp.route('')
def home():
    return render_template('home.html')

#odds must go here  