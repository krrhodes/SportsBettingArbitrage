import smtplib
from datetime import date
from email.message import EmailMessage


DEFAULT_EMAIL_ADDRESS = 'kenai.rhodes@gmail.com'

TEMPLATE = """
Hello,

The following arbitrage opurtunities have been found today:

"""


def report_results(results, send_email, email=DEFAULT_EMAIL_ADDRESS):
	if not results:
		print("No Arbitrage Oppurtunities Found")
		return

	contents = TEMPLATE
	for result in results:
		contents += f"""
			Bet {result['home_team_bet']} on {result['home_team']['name']} with {result['home_team']['max_odds']['bookmaker']}
			and {result['away_team_bet']} on {result['away_team']['name']} with {result['away_team']['max_odds']['bookmaker']}
			for a guranteed profit of {result['projected_profit']}\n\n
		"""

	print(contents)

	if send_email:
		msg = EmailMessage()

		msg['Subject'] = f"Sports Betting Arbitrage Oppurtunities for {date.today()}"
		msg['From'] = email
		msg['To'] = email
		msg.set_content(contents)

		s = smtplib.SMTP('localhost')
		try:
			s.send_message(msg)
		except Exception as e:
			print(f"Error sending email: {e}")
		finally:
			s.quit()
