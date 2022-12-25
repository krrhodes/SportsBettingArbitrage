import sys

import API
import Arbitrage
import Reporter


def main():
	__validate_args()
	sport = sys.argv[1]

	odds = API.get_odds(sport)
	oppurtunities = Arbitrage.get_arbitrage_oppurtunities(odds, True)
	Reporter.report_results(oppurtunities, True)


def __validate_args():
	if not 2 <= len(sys.argv) <= 3:
		print("Usage: python SportsBettingArbitrage <Sport Name> <Email | none>")
		quit()


if __name__ == "__main__":
	main()
