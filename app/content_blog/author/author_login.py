import flask
from flask import Blueprint
from flask_cors import cross_origin


author_login_bp = Blueprint('author_login', __name__, url_prefix = '/author')

@author_login_bp.route('/login')
def author_login():
    return "check db for author id or null, then use auth0 to verify login info"
