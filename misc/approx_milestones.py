# This is a one off script.
# Attempt approximating the milestone an issue would have landed in
#   based on the completion date and some leftover data I found in my GitLab boards.
import json
from datetime import datetime,date

def main():
    trello = {}
    date_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"

    with open('export-trello.json', 'r') as f: 
        trello = json.load(f)

    # I only close issues on my 'Main' board, so hardcode index   
    cards = sorted([c for c in trello[0]['issues'] if not c['is_open']], key=lambda i: i['completed_date'])
    lowest = datetime.strptime(cards[0]['completed_date'], date_fmt)
    for card in cards:
        card_date = datetime.strptime(card['completed_date'], date_fmt)
        print("{}   {}  {} -> milestone {}".format(
            card['identifier'],
            card['name'][:25].rjust(25,' '), 
            card['completed_date'], 
            ((card_date - lowest).days // 7) + 1
        ))
    print("\nApproximated {} card(s)".format(len(cards)))
    print("Oldest card: {}".format(lowest))

if __name__ == "__main__":main()
