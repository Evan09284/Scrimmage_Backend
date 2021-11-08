import requests
import os
import json
import ast
from app.config import META_KEY
from flask import Blueprint


#temp script for populating db with team info

team_bp = Blueprint('team', __name__, url_prefix='/team')

#returns league codes stored in static json file 
@team_bp.route('')
def get_team_codes():

    json_data = open(os.path.join('app/betting', "league_codes.json"), "r")
    teams_data = json.load(json_data)
    
    teams = teams_data.get('data')
    all_data = []
    
    for t in teams:
        for abv in t:
            print(abv)
            parameters = {
                'sport': abv,
                'apiKey': META_KEY,
            }

            req = requests.get(
                f'https://scrimmage.api.areyouwatchingthis.com/api/teams.json?',
                params=parameters
            )

            data = req.json().get('results')
            if data is not None and len(data):
                
                for team in data:

                    team_data = {
                        'team_name': team.get('name'),
                        'initials': team.get('initials'),
                        'city': team.get('city'),
                        'team_ID': team.get('teamID'),
                        'sport_acronym': team.get('sport'),
                        'league_code': team.get('leagueCode')
                    }

                    all_data.append(team_data)

    return {'data': all_data}
