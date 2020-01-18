# This is a one off script.
# Attempt approximating the milestone an issue would have landed in
#   based on the completion date and some leftover data I found in my GitLab boards.

import json
from datetime import datetime,date

def main():
    trello = []
    date_fmt = "%Y-%m-%dT%H:%M:%S.%fZ"

    with open('export.json', 'r') as f: 
        trello = json.load(f)

    # I only close issues on my 'Main' board, so hardcode index
    closed = sorted([c for c in trello[0]['issues'] if not c['is_open']], key=lambda i: i['completed_date'])
    lowest = datetime.strptime(closed[0]['completed_date'], date_fmt)
    new_cards,milestones = [],[]

    for card in trello[0]['issues']:
        if not card['is_open']:
            card_date = datetime.strptime(card['completed_date'], date_fmt)
            milestone = ((card_date - lowest).days // 7) + 1
            print("{}   {}  {} -> milestone {}".format(
                card['identifier'],
                card['name'][:25].rjust(25,' '), 
                card['completed_date'], 
                milestone
            ))
            card['milestone_id'] = milestone
            milestones.append({'name': "Week {}".format(milestone), 'id': milestone})
        new_cards.append(card)

    print("\nApproximated milestone for {} card(s)".format(len(closed)))
    print("Oldest card: {}".format(lowest))

    trello[0]['issues'] = sorted(new_cards, key=lambda i: i['milestone_id'])
    trello[0]['milestones'] = sorted([dict(t) for t in {tuple(d.items()) for d in milestones}], key=lambda i: i['id'])

    with open('export.json', 'w+') as f:
        f.write(json.dumps(trello, indent=2))


if __name__ == "__main__":main()