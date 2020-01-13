import requests, json
import utils as utils

def populate_labels(config, gl_json):
    labels = []
    label_mapping = config["trello"]["label-mapping"]["gitlab"]
    headers = {"Content-Type": "application/json"}
    for label in gl_json["labels"]:
        name = label["name"]
        labels.append(label)
        if not name in label_mapping["ignore"]:
            params = {
              "name": name, 
              "color": label_mapping["colors"][name], 
              "idBoard": config["trello"]["boardId"],
              "token": config["trello"]["token"],
              "key": config["trello"]["apiKey"]
            }
            print("  POST " + params["name"] + " --- " + params["color"])
            requests.post(config["trello"]["url"]+"labels", headers=headers, params=params)
    return labels

def get_board_labels(url, creds):
    return requests.get(url, headers={"Content-Type": "application/json"}, params=creds).json()

def migrate_issues(config, mapped_json):
    headers = {"keepFromSource": "all", "Content-Type":"application/json"}
    params = {"token": config["trello"]["token"], "key": config["trello"]["apiKey"]}
    for card in mapped_json["cards"]:
        params["idList"] = card["idList"]
        print(card)
        requests.post(config["trello"]["url"]+"cards",headers=headers,params=params,data=json.dumps(card))

def map_gl_to_trl(config, gl_json):
    cards = []
    label_mapping = config["trello"]["label-mapping"]["gitlab"]
    print("Mapping GitLab issues to Trello cards...")
    populate_labels(config, gl_json)

    labels_url = config["trello"]["url"] + "/boards/{}/labels".format(config["trello"]["boardId"])
    creds = {"token": config["trello"]["token"], "key": config["trello"]["apiKey"]}

    board_labels = get_board_labels(labels_url, creds)
    if len(board_labels) == 0 or True:
        for issue in gl_json["issues"]:
            new_card = {
              "idMembers": config["trello"]["memberId"],
              "name": issue["title"],
              "idLabels": []
            }
            if issue["description"]: 
                new_card["desc"] = issue["description"]
            if issue["closed_at"]:
                new_card["due"] = issue["closed_at"]
                new_card["dueComplete"] = True
                new_card["idList"] = config["trello"]["list-mapping"]["gitlab"]["closedId"]
            else:
                new_card["idList"] = config["trello"]["list-mapping"]["gitlab"]["openId"]
            for label in board_labels:
                if not label["name"] in label_mapping["ignore"] and label["name"] in issue["labels"]:
                    new_card["idLabels"].append(label["id"])
            cards.append(new_card)
    return {"labels": board_labels, "cards": cards}

def main():
    config = utils.read_file_json("./config.json")
    file_path = "{}gitlab-{}.json".format(utils.end_with(config["save-path"],"/"), config["gitlab"]["projId"])
    mapped_json = map_gl_to_trl(config, utils.read_file_json(file_path))
    migrate_issues(config, mapped_json)
    save_path = utils.end_with(config["save-path"],"/") + "gitlab-trello-{}.json".format(config["gitlab"]["projId"])
    utils.write_file_json(save_path, mapped_json)

if __name__ == "__main__": main()