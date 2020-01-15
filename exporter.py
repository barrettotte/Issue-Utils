import os,sys,requests
import utils as utils
from models.issue import Issue

def show_findings(labels, lists, opened, closed):
    print("    Found {:4d} active label(s)".format(len(labels)))
    print("    Found {:4d} active list(s)".format(len(lists)))
    print("    Found {:4d} open card(s)".format(len(opened)))
    print("    Found {:4d} closed card(s)".format(len(closed)))


def export_trello(config, board_configs, out_path):
    print("Exporting Trello boards...")
    boards = []
    params = {'key': config['key'], 'token': config['token']}
    for bc in board_configs:
        print("  Exporting board '{}'...".format(bc['name']))
        board_url = "{}/boards/{}".format(config['url'], bc['id']['trello'])
        resp = requests.get(board_url, params=params).json()
        
        resp_labels = resp['labelNames']
        labels = [{l: resp_labels[l]} for l in resp_labels if resp_labels[l] != '']
        resp_lists = requests.get(board_url + "/lists", params=params).json()
        lists = [{'name': l['name'], 'id': l['id']} for l in resp_lists if not l['closed']]
        
        opened = requests.get(board_url, params={**params, **{"cards":"visible"}}).json()["cards"]
        closed = requests.get(board_url, params={**params, **{"cards":"closed"}}).json()["cards"]
        show_findings(labels, lists, opened, closed) # DEBUG

        issues = []
        [issues.append(Issue(o, 'trello').__dict__) for o in opened]
        [issues.append(Issue(c, 'trello').__dict__) for c in closed]
        boards.append({'labels': labels, 'lists': lists, 'issues': issues})
    return boards


def main():
    config = utils.read_file_json("./config.json")
    boards, out_path = config['boards'], config['export']

    exported = export_trello(config['trello'], boards, out_path)
    utils.write_file_json("{}{}export-trello.json".format(out_path, os.path.sep), exported)
    

if __name__ == "__main__":main()