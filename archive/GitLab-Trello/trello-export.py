import requests
import utils as utils

def get_trl_json(board_url, params):
    print("Exporting Trello board cards...")
    trl_json = requests.get(board_url, params=params).json()
    print("Found {} label(s)".format(len(trl_json["labelNames"])))
    trl_json["open-cards"] = requests.get(board_url, params={**params,**{"cards":"visible"}}).json()["cards"]
    trl_json["closed-cards"] = requests.get(board_url, params={**params,**{"cards":"closed"}}).json()["cards"]
    print("Found {} open card(s)".format(len(trl_json["open-cards"])))
    print("Found {} closed card(s)".format(len(trl_json["closed-cards"])))
    # batches of 1000 cards ?
    return trl_json

def main():
    config = utils.read_file_json("./config.json")
    creds = {"key": config["trello"]["apiKey"], "token": config["trello"]["token"]}
    board_url = utils.end_with(config["trello"]["url"],"/") + "boards/" + config["trello"]["boardId"]
    trl_json = get_trl_json(board_url, creds)
    save_path = utils.end_with(config["save-path"],"/") + "trello-{}.json".format(config["trello"]["boardId"])
    utils.write_file_json(save_path, trl_json)

if __name__ == "__main__":main()