import requests
from app.config import META_KEY, rd
from flask import Blueprint
import ast


# retrieves all games across al sports. Returns gameID, leagueCode, teamIDs, scores, and time left
scores_bp = Blueprint('scores', __name__, url_prefix='/scores')


@scores_bp.route('/get', methods=['GET'])
def get_scores():
    """Endpoint to list scores from Redis"""

    data = rd.get('scores')

    if data:
        data_str = data.decode("utf-8")
        data_json = ast.literal_eval(data_str)
        response = {'data': data_json}
        status = 200
    else:
        response = {'data': "no data"}
        status = 404

    return response, status
