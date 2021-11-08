import os
import requests
import json
from flask import Blueprint
from app.config import META_KEY, rd
import ast

odds_bp = Blueprint('odds', __name__, url_prefix='/odds')


@odds_bp.route('/get', methods=['GET'])
def get_odds():
    """Endpoint to list odds from Redis"""

    data = rd.get('odds')

    if data:
        data_str = data.decode("utf-8")
        data_json = ast.literal_eval(data_str)
        response = {'data': data_json}
        status = 200
    else:
        response = {'data': "no data"}
        status = 404

    return response, status
