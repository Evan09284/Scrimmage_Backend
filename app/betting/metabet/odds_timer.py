import os
import requests
import json

from app import socketio
from app.config import META_KEY, rd
import pydash
import time

from app.models import UserBet, NotificationStatusEnum, db


def update_odds():
    """Endpoint to update odds on Redis"""

    leagues = [
        'ncaabaseball',
        'ncaaf',
        'golf',
        'mlb',
        'mma',
        'nfl',
        'nhl',
        'soccer',
        'tennis', 
        'wnba',
        'ncaabw',
        'esports'
    ]

    all_league_data = []

    for league in leagues:

        json_data = open(os.path.join(
            'app/betting/json_scripts', 'league_codes.json'), 'r')
        teams_data = json.load(json_data).get('data')

        *misc, = []
        for teams in teams_data:
            *abv, = teams
            misc.append(abv)

        parameters = {
            'sport': league,
            'apiKey': META_KEY
        }

        req = requests.get(
            f'https://scrimmage.api.areyouwatchingthis.com/api/odds.json?',
            params=parameters)

        # checks to see if there are results at all
        results = req.json().get('results')
        if results == []:
            continue

        data = []
        if len(results) > 1:

            for game_data in results:

                """INITIATES ARRAYS FOR EACH BET TYPE"""
                spreadTeam1array = []
                spreadTeam2array = []
                overarray = []
                underarray = []
                moneylineTeam1array = []
                moneylineTeam2array = []

                game_id = game_data.get('gameID')
                date_and_time = game_data.get('date')
                # removes the miliseconds from the time. Gets to seconds
                if date_and_time:
                    date_and_time = round(date_and_time/1000, None)
                odds = game_data.get('odds')
                for sportbook in odds:

                    """RETRIEVES DATA"""
                    book = (sportbook.get('provider'))
                    spreadLine1 = sportbook.get('spreadLine1')
                    spreadTeam1 = sportbook.get('spread')
                    spreadLine2 = sportbook.get('spreadLine2')
                    try:
                        spreadTeam2 = float(spreadTeam1)*-1
                    except TypeError:
                        spreadTeam2 = None
                    overLine = sportbook.get('overUnderLineOver')
                    underLine = sportbook.get('overUnderLineUnder')
                    OverUnderHandicap = sportbook.get('overUnder')
                    moneylineTeam1 = sportbook.get('moneyLine1')
                    moneylineTeam2 = sportbook.get('moneyLine2')

                    # converts decimal price to american price and stores both
                    def decimal_to_american(decimal_price):
                        if decimal_price > 2:
                            american_price = round(
                                (decimal_price - 1) * 100, None)
                        else:
                            american_price = round(-100 /
                                                   (decimal_price - 1), None)
                        return american_price

                    """ CHECKS IF THERE IS SPREAD DATA 
                        AND APPENDS TO EACH BET TYPE ARRAY """
                    if (spreadLine1 == None or 
                        spreadTeam1 == None or 
                        book == 'CONSENSUS'):
                        pass
                    else:
                        american_price = decimal_to_american(spreadLine1)
                        spreadTeam1array.append(
                            {
                                'handicap': spreadTeam1, 
                                'american_price': american_price, 
                                'decimal_price': spreadLine1, 
                                'book': book
                            }
                        )
                        american_price = decimal_to_american(spreadLine1)

                    if (spreadLine2 == None or 
                        spreadTeam2 == None or 
                        book == 'CONSENSUS'):
                        pass
                    else:
                        american_price = decimal_to_american(spreadLine2)
                        spreadTeam2array.append(
                            {
                                'handicap': spreadTeam2,
                                'american_price': american_price,
                                'decimal_price': spreadLine2,
                                'book': book
                            }
                        )

                    """ CHECKS IF THERE IS OVER/UNDER DATA 
                        AND APPENDS TO EACH BET TYPE ARRAY """
                    if (overLine == None or 
                        OverUnderHandicap == None or 
                        book == 'CONSENSUS'):
                        pass
                    else:
                        american_price = decimal_to_american(overLine)
                        overarray.append(
                            {
                                'handicap': OverUnderHandicap, 
                                'american_price': american_price, 
                                'decimal_price': overLine, 
                                'book': book
                            }
                        )

                    if (underLine == None or 
                        OverUnderHandicap == None or 
                        book == 'CONSENSUS'):
                        pass
                    else:
                        american_price = decimal_to_american(underLine)
                        underarray.append(
                            {
                                'handicap': OverUnderHandicap,
                                'american_price': american_price,
                                'decimal_price': underLine,
                                'book': book
                            }
                        )

                    """ CHECKS IF THERE IS MONEYLINE DATA 
                        AND APPENDS TO EACH BET TYPE ARRAY """
                    if moneylineTeam1 == None or book == 'CONSENSUS':
                        pass
                    else:
                        american_price = decimal_to_american(moneylineTeam1)
                        moneylineTeam1array.append(
                            {
                                'american_price': american_price,
                                'decimal_price': moneylineTeam1,
                                'book': book
                            }
                        )

                    if (moneylineTeam2 == None or 
                        moneylineTeam2 == 'None' or 
                        book == 'CONSENSUS'):
                        pass
                    else:
                        american_price = decimal_to_american(moneylineTeam2)
                        moneylineTeam2array.append(
                            {
                                'american_price': american_price,
                                'decimal_price': moneylineTeam2,
                                'book': book
                            }
                        )

                """SORTS EACH BET TYPE ARRAY BY HIGHEST LINE VALUE FIRST"""
                spreadTeam1array.sort(
                    key=lambda x: x['decimal_price'], reverse=True)

                spreadTeam2array.sort(
                    key=lambda x: x['decimal_price'], reverse=True)

                overarray.sort(key=lambda x: x['decimal_price'], reverse=True)
                underarray.sort(key=lambda x: x['decimal_price'], reverse=True)

                moneylineTeam1array.sort(
                    key=lambda x: x['decimal_price'], reverse=True)
                    
                moneylineTeam2array.sort(
                    key=lambda x: x['decimal_price'], reverse=True)

                """APPENDS ODDS DATA FOR THAT GAME"""
                odds_data = [
                    {f'{game_id}-spreadTeam1': spreadTeam1array}, 
                    {f'{game_id}-spreadTeam2': spreadTeam2array}, 
                    {f'{game_id}-over': overarray}, 
                    {f'{game_id}-under': underarray},
                    {f'{game_id}-moneylineTeam1': moneylineTeam1array},
                    {f'{game_id}-moneylineTeam2': moneylineTeam2array}
                ]

                game = {
                    'game_id': game_id,
                    'date_and_time': date_and_time,
                    'team_name_1': game_data.get('team1Name'),
                    'team_id_1': game_data.get('team1ID'),
                    'team_initials_1': game_data.get('team1Initials'),
                    'team_city_1': game_data.get('team1City'),
                    'team_name_2': game_data.get('team2Name'),
                    'team_id_2': game_data.get('team2ID'),
                    'team_initials_2': game_data.get('team2Initials'),
                    'team_city_2': game_data.get('team2City'),
                    'league_code': game_data.get('leagueCode'),
                    'odds': odds_data
                }
                data.append(game)

        # sorts the games by date and time with closest to occur games at the top
        data.sort(key=lambda x: x['date_and_time'])

        all_league_data.append({league: data})

    # Update scores if there's any
    scores = update_scores()

    # update league data with scores
    if scores:
        all_league_data = update_all_league_data(all_league_data, scores)

    # TODO: check data persistence
    try:
        rd.set('odds', str(all_league_data))
        response = "Odds updated successfully"
        status = 201
    except Exception as e:
        response = f"Error saving odds: {e}"
        status = 422

    return response, status


def update_scores():
    """Endpoint to update scores on Redis"""

    req = requests.get(
        f'https://scrimmage.api.areyouwatchingthis.com/api/games.json?apiKey={META_KEY}'
    )
    data = req.json().get('results')

    scores_data = []
    for d in data:

        team_1_score = d.get('team1Score')
        time_left = d.get('timeLeft')
        gameID = d.get("gameID")

        if time_left is not None and team_1_score is not None:
            scores = {
                'gameID': gameID,
                'team1score': team_1_score,
                'team2score': d.get("team2Score"),
                'time_left': time_left
            }

            scores_data.append(scores)

    return scores_data


def update_all_league_data(lg_data, scores):
    """Update all league odds with score info"""
    key_list = pydash.flatten_deep(lg_data['data'][0])

    for league in lg_data:
        # Loop over league's names
        for name in key_list:
            # Loop over all odds and scores
            for odd, score in zip(league[name], scores):
                # Check if odd has score's game_id
                if odd['game_id'] == score['gameID']:
                    # Update odd with score info
                    odd.update(score)
                    # Remove duplicated gameID
                    del odd['gameID']

    return lg_data


def compare_notification_price():
    from app import create_app
    app = create_app()
    price_data = [2.3, 2.4, 2.6, 2.7, 2.4, 2.8]
    with app.app_context():
        while price_data:
            current_price = price_data.pop(0)

            UserBet.query.filter(
                UserBet.notification_status == {NotificationStatusEnum.inactive.value},
                UserBet.notification_price > current_price
            ).update({UserBet.notification_status: {NotificationStatusEnum.scheduled.value}})

            db.session.commit()
            time.sleep(10)
    return


@socketio.on('notification_confirm')
def notification_confirm(json):
    from app import create_app
    app = create_app()
    with app.app_context():
        UserBet.query.filter(
            UserBet.id == json['id']
        ).update({UserBet.notification_status: {NotificationStatusEnum.notified.value}})

        db.session.commit()
        print(json)


def price_notifying():
    from flask_socketio import SocketIO, emit
    from app import create_app

    app = create_app()
    socketio = SocketIO()
    socketio.init_app(app)

    with app.app_context():
        bets = UserBet.query.filter(
            UserBet.notification_status == {NotificationStatusEnum.scheduled.value}
        ).all()
        for bet in bets:
            socketio.emit('price_notification', bet.as_dict(), namespace='/', broadcast=True)

    return
