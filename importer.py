import os, sys, requests, json, time
import utils as utils
from models.issue import Issue


trello_rgb = {
    'yellow': [255, 255,   0], 'purple': [153,   0, 204],
    'blue':   [  0, 102, 255], 'red':    [204,   0,   0],
    'green':  [  0, 153,   0], 'orange': [255, 153,   0],
    'black':  [  0,   0,   0], 'sky':    [  0, 204, 255],
    'pink':   [255,  51, 153], 'lime':   [102, 255,  51]
}


def post_glo(url, body, token):
    rate_limiter = 1.10  # 2500 requests / 3600 seconds
    headers = {'Content-Type': 'application/json'}
    params = {'access_token': token}
    time.sleep(rate_limiter)
    resp = requests.post(url, headers=headers, params=params, data=body)
    if resp.status_code in [200,201]: 
        return resp.json()
    utils.print_response(resp)
    if resp.status_code == 429:
        raise Exception("POST ({}) Glo rate limit hit.".format(resp.status_code))
    raise Exception("Glo POST failed ({})".format(resp.status_code))


# TODO: break this nasty function up!
def import_glo(config, boards):
    print('Importing boards to Glo...')
    token = config['token']
    base_url = "{}/boards".format(config['url'])

    for board in boards:
        columns,milestones = board['columns'],board['milestones']
        labels,issues = board['labels'],board['issues']
        
        print("  Importing board '{}'".format(board['name']))
        new_board = post_glo(base_url, json.dumps({'name': board['name']}), token)
        board_url = base_url + "/" + new_board['id']

        label_xrefs = []
        print("    Importing {} label(s)".format(len(labels)))
        for idx,label in enumerate(labels):
            print("      Importing label '{}'  [{} of {}]".format(label['name'], idx+1, len(labels)))
            rgb = trello_rgb[label['color']]
            label_body = {'name': label['name'], 'color': {'r': rgb[0], 'g': rgb[1], 'b': rgb[2]}}
            new_label = post_glo(board_url + '/labels', json.dumps(label_body), token)
            label_xrefs.append({'new_id': new_label['id'], 'old_id': label['id']})

        col_xrefs = []
        print("    Importing {} column(s)".format(len(columns)))
        for idx,col in enumerate(columns):
            print("      Importing column '{}'  [{} of {}]".format(col['name'], idx+1, len(columns)))
            new_col = post_glo(board_url + '/columns', json.dumps({'name': col['name']}), token)
            col_xrefs.append({'new_id': new_col['id'], 'old_id': col['id']})

        ms_xrefs = []
        print("    Importing {} milestone(s)".format(len(milestones)))
        for idx,ms in enumerate(milestones):
            print("      Importing milestone '{}'  [{} of {}]".format(ms['name'], idx+1, len(milestones)))
            ms_body = {'name': ms['name'], 'state': 'open' if idx == len(milestones)-1 else 'closed'}
            new_ms = post_glo(board_url + '/milestones', json.dumps(ms_body), token)
            ms_xrefs.append({'new_id': new_ms['id'], 'old_id': ms['id']})

        print("    Importing {} issue(s)".format(len(issues)))
        for idx,issue in enumerate(sorted(board['issues'], key=lambda i: i['milestone_id'], reverse=True)):
            print("      Importing issue '{}'  [{} of {}]".format(ms['name'], idx+1, len(issues)))
            issue_body = {'name': issue['name'], 'desc': issue['description'],
                'assignees': [{'id': config['user']}], 'due_date': issue['completed_date']}
            
            if issue['column_id'] != -1:
                issue_body['column_id'] = [x['new_id'] for x in col_xrefs if x['old_id'] == issue['column_id']][0]

            if issue['milestone_id'] != -1:
                issue_body['milestone_id'] = [x['new_id'] for x in ms_xrefs if x['old_id'] == issue['milestone_id']][0]
            # TODO: LABELS

            if issue['creation_date']:
                issue_body['creation_date'] = issue['creation_date']
            if issue['completed_date'] and not issue['is_open']:
                issue_body['archived_date'] = issue['completed_date']

            new_issue = post_glo(board_url + '/cards', json.dumps(issue_body), token)
            
            break # TODO: debug
        break #TODO: debug


def main():
    config = utils.read_file_json('./config.json')
    out_path = config['export']
    target = 'glo'   # TODO: Make CLI

    if target == 'glo':
        import_glo(config['glo'], utils.read_file_json(out_path + os.sep + 'export.json'))
    else:
        raise Exception("Unsupported target '{}'".format(target))


if __name__ == "__main__":main()