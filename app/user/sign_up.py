import json
from flask import Blueprint
from flask_cors import cross_origin

signup_bp = Blueprint('sign_up', __name__, url_prefix='/user')

#Auth0 check + add user to db, change into post req
@signup_bp.route('/sign_up')
def sign_up():
    return 'auth0 stuff done here'
