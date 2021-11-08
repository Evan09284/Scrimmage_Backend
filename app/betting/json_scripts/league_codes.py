import requests
import os
from flask import Blueprint
from app.config import META_KEY


# retrieves the codes associated with each league and stores in json format

def get_league_codes():

    parameters = {
        'apiKey': META_KEY
    }

    req = requests.get(
        f'https://scrimmage.api.areyouwatchingthis.com/api/sports.json?',
        params=parameters
    )

    
    data = req.json().get('results')

    sport_data = []

    for sport in data:
        d = []
        abv_data = sport.get('abbreviation')
        for s in sport['leagues']:
            s_data = {
                'name': s.get('name'),
                'code': s.get('code')
            }
            d.append(s_data)
        result = {abv_data: d}
        sport_data.append(result.copy())
    return {'data': sport_data}
            
