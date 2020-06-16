import json

def main():
  all_issues = []
  all_labels = []
  records = []

  with open('export.json', 'r') as f:
    
    for board in json.load(f):
      all_labels += board['labels']
      all_issues += board['issues']

    i = 0
    for issue in all_issues:
      if issue['milestone_id'] > 0:
        s =  "[{}]  {}  {}  [".format(
          str(issue['milestone_id']).rjust(2, '0'), 
          issue['name'][:50].ljust(50, ' '), 
          issue['due_date'][:10]
        )

        labels = []
        for label_idx in issue['labels']:
          l = None
          for l in all_labels:
            if l['id'] == label_idx:
              labels.append(l['name'])
              break

        s += ', '.join(labels) + ']'

        records.append(s)

  with open('report.txt', 'w') as f:
    f.write('\n'.join(records))

  print('{} total issue(s)'.format(len(all_issues)))

if __name__ == "__main__": main()