import flask
from flask import Blueprint
from flask_cors import cross_origin


author_signup_bp = Blueprint('author_signup', __name__, url_prefix='/author')

@author_signup_bp.route('/signup')
def author_signup():
    return 'db check for null, use auth0 to register and then add author id to db'
    