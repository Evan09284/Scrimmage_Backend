import flask
from flask import Blueprint
from flask_cors import cross_origin


tracker_bp = Blueprint('tracker', __name__, url_prefix='/tracker')

@tracker_bp.route('')
def display_tracker():
    return 'tracker script run here'