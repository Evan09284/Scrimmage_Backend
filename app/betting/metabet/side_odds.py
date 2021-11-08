import json
import requests
from datetime import datetime, timedelta
import time


from flask import Blueprint
from app.config import META_KEY

side_odds_bp = Blueprint('side_odds', __name__, url_prefix='/side_odds')


@side_odds_bp.route('')
def get_side_odds():
    # side odds needs to be sent a gameID
    parameters = {
        'gameID': 485092,  # change back to gameID variable
        'apiKey': META_KEY,

    }

    req = requests.get(
        f'https://scrimmage.api.areyouwatchingthis.com/api/sideodds.json?',
        params=parameters)

    data = req.json()
    results = data.get('results')
    if results == []:
        return ({'data': 'no data'})

    players = {}
    unique_player_ids = {}
    player_data = data.get('players')
    for player in player_data:
        playerID = player.get('playerID')
        first_name = player.get('firstName')
        last_name = player.get('lastName')
        teamID = player.get('teamID')
        position = player.get('position')

        players[playerID] = {
            'playerID': playerID,
            'first_name': first_name,
            'last_name': last_name,
            'teamID': teamID,
            'position': position
        }

        unique_player_ids[playerID] = {}

    side_odd_data = []
    for bet_type in results:
        title = bet_type.get('title')
        code = bet_type.get('type')

        for side_odd in bet_type['sideOdds']:
            sportsbook = side_odd.get('provider')
            # don't need consensus
            if sportsbook == 'CONSENSUS':
                continue

            handicap = side_odd.get('value')

            # price is listed for single outcome bet types
            price = side_odd.get('price')
            # price 1 and 2 are for multi outcome bet types
            price1 = side_odd.get('price1')
            price2 = side_odd.get('price2')

            # if it is a single outcome bet it makes price1 that value for sorting later
            if price1 == None and price != None:
                price1 = price

            # if there are no prices we skip so we don't show the data
            if price1 == None and price2 == None:
                continue

            url = side_odd.get('url')
            playerID_from_side_odds = side_odd.get('playerID')

            try:
                player_info = players[playerID_from_side_odds]
            except KeyError:
                pass

            player_first_name = player_info['first_name']
            player_last_name = player_info['last_name']
            player_position = player_info['position']

            sportsbook_data = {
                'title': title, 
                'playerID': playerID_from_side_odds, 
                'first_name': player_first_name, 
                'last_name': player_last_name, 
                'player_position': player_position,
                'sportsbook': sportsbook, 
                'handicap': handicap, 
                'price1': price1, 
                'price2': price2, 
                'url': url
            }

            side_odd_data.append(sportsbook_data)

            # this is alternative I am working with. It returns a better organized more nested dictionary
            if playerID_from_side_odds in unique_player_ids:
                if title in unique_player_ids[playerID_from_side_odds]:
                    unique_player_ids[playerID_from_side_odds][title].append(
                        sportsbook_data)
                else:
                    unique_player_ids[playerID_from_side_odds][title] = [
                        sportsbook_data]

            # may want to add something in this else
            else:
                pass

    # sorts by player, then what the bet is on, then price with highest first
    side_odd_data.sort(key=lambda x: (
        x['playerID'], x['title'], x['price1']), reverse=True)

    # I still need to sort the unique player dictionary by price

    return {'data': side_odd_data}
