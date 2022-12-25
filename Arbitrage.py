
BASE_UNIT_SIZE = 100


# Result Object:
# {
#     'home_team' : {
# 		'name'    : 'STRING',
# 		'max_odds' : {
# 			'bookmaker' : 'STRING',
# 			'odds'      : NUMBER,
# 		},
# 	},
# 	'away_team' : {
# 		'name'    : 'STRING',
# 		'max_odds' : {
# 			'bookmaker' : 'STRING',
# 			'odds'      : NUMBER,
# 		},
# 	},
# 	'home_team_bet'      : NUMBER,
# 	'away_team_bet'      : NUMBER,
#   'projected_profit'   : NUMBER,
# }
def get_arbitrage_oppurtunity(game_odds):
	result = {}

	home_team = game_odds['home_team']
	away_team = game_odds['away_team']
	result['home_team'] = {}
	result['home_team']['name'] = home_team
	result['away_team'] = {}
	result['away_team']['name'] = away_team

	max_home_team_odds = max(
		[bookmakersOdds for bookmakersOdds in game_odds['bookmakers']],
		key=lambda k: k['markets'][0]['outcomes'][0]['price']
	)
	result['home_team']['max_odds'] = {}
	result['home_team']['max_odds']['bookmaker'] = max_home_team_odds['title']
	result['home_team']['max_odds']['odds'] = max_home_team_odds['markets'][0]['outcomes'][0]['price']

	max_away_team_odds = max(
		[bookmakersOdds for bookmakersOdds in game_odds['bookmakers']],
		key=lambda k: k['markets'][0]['outcomes'][1]['price']
	)
	result['away_team']['max_odds'] = {}
	result['away_team']['max_odds']['bookmaker'] = max_away_team_odds['title']
	result['away_team']['max_odds']['odds'] = max_away_team_odds['markets'][0]['outcomes'][1]['price']

	home_team_first_profit = __calculate_profit(
		result['home_team']['max_odds']['odds'],
		result['away_team']['max_odds']['odds']
	)
	away_team_first_profit = __calculate_profit(
		result['away_team']['max_odds']['odds'],
		result['home_team']['max_odds']['odds']
	)
	if home_team_first_profit >= away_team_first_profit:
		result['home_team_bet'] = BASE_UNIT_SIZE
		result['away_team_bet'] = __calculate_second_bet(
			result['home_team']['max_odds']['odds'],
			result['away_team']['max_odds']['odds']
		)
	else:
		result['away_team_bet'] = BASE_UNIT_SIZE
		result['home_team_bet'] = __calculate_second_bet(
			result['away_team']['max_odds']['odds'],
			result['home_team']['max_odds']['odds']
		)

	result['projected_profit'] = max(home_team_first_profit, away_team_first_profit)

	return result


def get_arbitrage_oppurtunities(game_odds, filter_negative_odds):
	result = [get_arbitrage_oppurtunity(odd) for odd in game_odds]

	result.sort(reverse=True, key=lambda k: k['projected_profit'])

	if filter_negative_odds:
		result = [descrepency for descrepency in result if descrepency['projected_profit'] > 0]

	return result


def __calculate_profit(odds1, odds2):
	second_bet = __calculate_second_bet(odds1, odds2)
	return ((BASE_UNIT_SIZE*odds1)-BASE_UNIT_SIZE) - second_bet


def __calculate_second_bet(odds1, odds2):
	return (BASE_UNIT_SIZE*odds1) / odds2
