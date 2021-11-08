from flask import Blueprint, request
from flask_cors import cross_origin
from app.models import UserBet, db

# only submit info -- not able to edit or delete
# rerenders new form auto

bet_slip_bp = Blueprint('bet_slip', __name__, url_prefix='/bets')


@bet_slip_bp.route('/betlog/<user_id>', methods=['GET'])
def get_bet_slip(user_id):
    """Endpoint to list user bets"""

    active_wager = request.args.get('active_wager')

    if active_wager:
        bets = UserBet.query.filter(
            UserBet.user_id==user_id,
            UserBet.active_wager==active_wager
        ).all()  
    else:
        bets = UserBet.query.filter(UserBet.user_id==user_id).all()  
    
    bets_json = [bet.as_dict() for bet in bets]    

    if bets_json:
        for item in bets_json:
            item['game_date'] = item['game_date'].strftime('%m/%d/%Y')
            item['bet_date'] = item['bet_date'].strftime('%m/%d/%Y')
            item['win_or_loss'] = item['win_or_loss'][0].value

        response = {'data': bets_json}
        return response, 200
    else:
        return "User id not found", 404


@bet_slip_bp.route('/trackbet/<user_id>', methods=['POST'])
def post_bet_slip(user_id):
    """Endpoint to save user bets"""

    body = request.get_json()
    try:
        user_bet = UserBet(
            event = body["event"],
            american_odds = body["american_odds"],
            decimal_odds = body["decimal_odds"],
            stake = body["stake"],
            sportsbook = body["sportsbook"],
            handicap = body["handicap"],
            notification_handicap = body["notification_handicap"],
            notification_price = body["notification_price"],
            closing_line_value = body["closing_line_value"],
            roi = body["roi"],
            results = body["results"],
            payout = body["payout"],
            game_date = body["game_date"],
            bet_date = body["bet_date"],
            user_id = user_id
        )

        db.session.add(user_bet)
        db.session.commit()

        user_bet_json = user_bet.as_dict()
        
        user_bet_json['game_date'] = user_bet_json['game_date'].strftime('%m/%d/%Y')
        user_bet_json['bet_date'] = user_bet_json['bet_date'].strftime('%m/%d/%Y')
        user_bet_json['win_or_loss'] = user_bet_json['win_or_loss'][0].value

        response = {'data': user_bet_json}

        return response, 201
    except Exception as e:
        return f"Error on POST: {e}", 400
