import json
import requests

API_BASE = 'https://api.the-odds-api.com'
API_KEY = '558c21044b135ca757d9ac470579023b'


def get_odds(sport, regions='us', markets='h2h'):
	response = requests.get(f"{API_BASE}/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions={regions}&markets={markets}")

	if response.status_code is not 200:
		raise Exception(response.text)
	else:
		return json.loads(response.text)
