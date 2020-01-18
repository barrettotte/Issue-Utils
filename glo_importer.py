import requests, json, time
import utils as utils
from models.issue import Issue

class Glo_Importer():

    def __init__(self, config):
        self.token = config['token']
        self.user = config['user']
        self.base_url = config['url']
        self.color_dict = {
          'yellow': [255, 255,   0],  'purple': [153,   0, 204],
          'blue':   [  0, 102, 255],  'red':    [204,   0,   0],
          'green':  [  0, 153,   0],  'orange': [255, 153,   0],
          'black':  [  0,   0,   0],  'sky':    [  0, 204, 255],
          'pink':   [255,  51, 153],  'lime':   [102, 255,  51]
        }


    def progress(self, idx, data, item_type):
        item = data[idx]
        identifer = item['id'] if 'id' in item else item['identifier']
        s = "      Importing {} '{}'".format(item_type, item['name'][:20]).ljust(50)
        s = "{} ({})".format(s, identifer).ljust(80)
        return "{} {} of {}".format(s, str(idx+1).rjust(4), str(len(data)).ljust(4))


    def find_id(self, target, ids):
        return [x['new_id'] for x in ids if x['old_id'] == target][0]


    def post(self, url, body, retry=0):
        rate_limiter = 1.10 
        headers = {'Content-Type': 'application/json'}
        params = {'access_token': self.token}

        time.sleep(rate_limiter)
        resp = requests.post(url, headers=headers, params=params, data=body)
        if resp.status_code in [200,201]: 
            return resp.json()
        utils.print_response(resp)

        if resp.status_code == 429:
            raise Exception("POST ({}) Glo rate limit hit.".format(resp.status_code))
        if resp.status_code == 502 and retry < 10:
            retry += 1
            print("POST ({}) Glo bad gateway. Retrying... {} of {}".format(resp.status_code, retry, 10))
            time.sleep(5)
            self.post(url, body, retry)
        raise Exception("Glo POST failed ({})".format(resp.status_code))


    def get_label_color(self, label):
        rgb = self.color_dict[label['color']]
        return {'r': rgb[0], 'g': rgb[1], 'b': rgb[2]}


    def import_labels(self, labels, url):
        ids = []
        print("    Importing {} label(s)".format(len(labels)))
        for idx,label in enumerate(labels):
            print(self.progress(idx, labels, 'label'))
            label_body = {'name': label['name'], 'color': self.get_label_color(label)}
            new_label = self.post(url, json.dumps(label_body))
            ids.append({'new_id': new_label['id'], 'old_id': label['id']})
        return ids


    def import_columns(self, columns, url):
        ids = []
        print("    Importing {} column(s)".format(len(columns)))
        for idx,col in enumerate(columns):
            print(self.progress(idx, columns, 'column'))
            new_col = self.post(url, json.dumps({'name': col['name']}))
            ids.append({'new_id': new_col['id'], 'old_id': col['id']})
        return ids


    def import_milestones(self, milestones, url):
        ids = []
        print("    Importing {} milestone(s)".format(len(milestones)))
        for idx,ms in enumerate(milestones):
            print(self.progress(idx, milestones, 'milestone'))
            ms_body = {
              'name': ms['name'], 
              'due_date': ms['due_date'],
              'state': 'open' # closed after issue imports
            }
            new_ms = self.post(url, json.dumps(ms_body))
            ids.append({'new_id': new_ms['id'], 'old_id': ms['id']})
        return ids


    def create_issue(self, issue, ids):
        new_issue = {
              'name': issue['name'],
              'description': {'text': issue['description'], 'created_by': {'id': self.user}},
              'board_id': issue['board_id'],
              'column_id': self.find_id(issue['column_id'], ids['column']),
              'assignees': [{'id': self.user}],
              'due_date': issue['due_date'],
              'created_by': {'id': self.user},
        }
        if not issue['is_open']:
            new_issue['archived_date'] = issue['completed_date']
        if len(issue['labels']) > 0:
            new_issue['labels'] = [{'id': self.find_id(lbl, ids['label'])} for lbl in issue['labels']]
        if issue['milestone_id'] != -1:
            new_issue['milestone'] = {'id': self.find_id(issue['milestone_id'], ids['milestone'])}
        return new_issue


    def import_issues(self, issues, url, ids):
        batch_size,batch_issues = 100,[]
        print("    Importing {} issue(s)".format(len(issues)))
        for idx,issue in enumerate(issues):
            print(self.progress(idx, issues, 'issue'))
            new_issue = self.create_issue(issue, ids)
            batch_issues.append(new_issue)
            if (idx+1) % batch_size == 0:
                print("    Sending batch {}-{} ...".format((idx+1)-batch_size, (idx+1)))
                self.post(url, json.dumps({'cards': batch_issues}))
                batch_issues = []
        if (idx+1) % batch_size != 0:
            print("    Sending batch {}-{} ...".format(len(issues) - ((idx+1) % batch_size), (idx+1)))
            self.post(url, json.dumps({'cards': batch_issues}))


    def import_boards(self, boards):
        print('Importing boards to Glo...')
        for board in boards:
            print("  Importing board '{}'".format(board['name']))
            new_board = self.post(self.base_url + "/boards", json.dumps({'name': board['name']}))
            board_url = self.base_url + "/boards/" + new_board['id']
            ids = {
              'label': self.import_labels(board['labels'], board_url + '/labels'),
              'column': self.import_columns(board['columns'], board_url + '/columns'),
              'milestone': self.import_milestones(board['milestones'], board_url + '/milestones')
            }
            issues = sorted(board['issues'], key=lambda i: i['milestone_id'], reverse=True)
            self.import_issues(issues, board_url + '/cards/batch', ids)
            time.sleep(3)

