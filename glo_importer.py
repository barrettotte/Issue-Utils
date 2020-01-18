import requests, json, time
import utils as utils
from models.issue import Issue


class Glo_Importer():

    def __init__(self, config):
        self.token = config['token']
        self.user = config['user']
        self.base_url = config['url']
        self.color_dict = {
          'yellow': [255, 255,   0], 'purple': [153,   0, 204],
          'blue':   [  0, 102, 255], 'red':    [204,   0,   0],
          'green':  [  0, 153,   0], 'orange': [255, 153,   0],
          'black':  [  0,   0,   0], 'sky':    [  0, 204, 255],
          'pink':   [255,  51, 153], 'lime':   [102, 255,  51]
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
            ms_body = {'name': ms['name'], 'state': 'open' if idx == len(milestones)-1 else 'closed'}
            new_ms = self.post(url, json.dumps(ms_body))
            ids.append({'new_id': new_ms['id'], 'old_id': ms['id']})
        return ids


    def import_issues(self, issues, url, ids):
        debug_idx = 0 
        print("    Importing {} issue(s)".format(len(issues)))
        col_ids,ms_ids,label_ids = ids['column'], ids['milestone'], ids['label']

        for idx,issue in enumerate(sorted(issues, key=lambda i: i['milestone_id'], reverse=True)):
            print(self.progress(idx, issues, 'issue'))
            new_issue = Issue(issue)
            
            if new_issue.column_id != -1:
                new_issue.column_id = self.find_id(new_issue.column_id, col_ids)
            if new_issue.milestone_id != -1:
                new_issue.milestone_id = self.find_id(new_issue.milestone_id, ms_ids)
            
            for i,lbl in enumerate(new_issue.labels):
                new_issue.labels[i] = {'id': self.find_id(lbl, label_ids)}

            # glo specific fields
            issue_body = new_issue.__dict__
            if new_issue.completed_date and not new_issue.is_open:
                issue_body['archived_date'] = new_issue.completed_date
            
            # clean up before request
            if len(issue_body['labels']) == 0:
                issue_body.pop('labels', None) # remove labels from body

            self.post(url, json.dumps(issue_body))

            # TODO:
            #   milestone id not being assigned correctly...

            # TODO: DEBUG
            debug_idx += 1
            if debug_idx == 8: break


    def import_boards(self, boards):
        print('Importing boards to Glo...')
        for board in boards:
            print("  Importing board '{}'".format(board['name']))
            new_board = self.post(self.base_url + "/boards", json.dumps({'name': board['name']}))
            board_url = self.base_url + "/boards/" + new_board['id']
            ids = {
              'label':     self.import_labels(board['labels'], board_url + '/labels'),
              'column':    self.import_columns(board['columns'], board_url + '/columns'),
              'milestone': self.import_milestones(board['milestones'], board_url + '/milestones')
            }
            self.import_issues(board['issues'], board_url + '/cards', ids)
            break #TODO: debug
