import os, sys, requests, time
import utils as utils
from models.issue import Issue


def show_findings(labels, milestones, columns, opened, closed):
    print("    Found {:4d} active label(s)".format(len(labels)))
    print("    Found {:4d} milestone(s)".format(len(milestones)))
    print("    Found {:4d} active columns(s)".format(len(columns)))
    print("    Found {:4d} open issue(s)".format(len(opened)))
    print("    Found {:4d} closed issue(s)".format(len(closed)))


def export_trello(config, boards, out_path):
    print("Exporting boards from Trello...")
    exported = []
    params = {'key': config['key'], 'token': config['token']}
    for board in boards:
        print("  Exporting board '{}'...".format(board['name']))
        board_url = "{}/boards/{}".format(config['url'], board['id']['trello'])
        resp_board = requests.get(board_url, params=params).json()

        labels = []
        resp_labels = requests.get(board_url + "/labels", params=params).json()
        for l in [x for x in resp_labels if x['id'] != '']:
            labels.append({k: l[k] for k in ['name','id','color'] if k in l})

        resp_cols = requests.get(board_url + "/lists", params=params).json()
        columns = [{'name': c['name'], 'id': c['id']} for c in resp_cols if not c['closed']]

        milestones = [] # trello has no milestones. See misc/approx_milestones.py
        
        opened = requests.get(board_url, params={**params, **{"cards":"visible"}}).json()["cards"]
        closed = requests.get(board_url, params={**params, **{"cards":"closed"}}).json()["cards"]
        show_findings(labels, [], columns, opened, closed)

        issues = []
        [issues.append(Issue(o, 'trello').__dict__) for o in opened]
        [issues.append(Issue(c, 'trello').__dict__) for c in closed]
        exported.append({
            'name': board['name'], 
            'id': resp_board['id'], 
            'labels': labels, 
            'milestones': milestones,
            'columns': columns, 
            'issues': issues
        })
    return exported


def main():
    exported = {}
    config = utils.read_file_json("./config.json")
    boards, out_path = config['boards'], config['export']
    target = 'trello'   # TODO: Make CLI

    if target == 'trello':
        exported = export_trello(config['trello'], boards, out_path)
    else:
        raise Exception("Unsupported target '{}'".format(target))
    
    utils.write_file_json("{}{}export.json".format(out_path, os.sep), exported)
    

if __name__ == "__main__":main()