import json

def main():
    total_issues = 0
    with open('export.json', 'r') as f: 
        for b in json.load(f): 
            total_issues += len(b['issues'])
    print('{} total issue(s)'.format(total_issues))

if __name__ == "__main__":main()