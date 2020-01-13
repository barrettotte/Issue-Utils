import requests
import utils as utils

def gitlab_batch(url, headers, item_type, batch_size):
    items = []
    url += item_type + "s/"
    init = requests.get(url, headers=headers).json()
    if not init or not init[0]:
        print("Initial {} request was empty; Skipping...".format(item_type))
    else:
        total = init[0]["iid"]
        print("Found {} {}(s)".format(total, item_type))
        for i in range(1, total, batch_size):
            rng = range(i, (i+batch_size if (i+batch_size<total) else total))
            print("  Exporting {}(s) in {}".format(item_type, rng))
            batch_url = "".join([(("?" if (b%batch_size==1) else "&") + "iids[]={}").format(b) for b in rng])
            items += [ms for ms in reversed(requests.get(url+batch_url, headers=headers).json())]
    return items

def get_gitlab_json(proj_url, token):
    print("Exporting GitLab project issues...")
    headers = {"PRIVATE-TOKEN":token}
    gl_json = requests.get(proj_url, headers=headers).json()
    gl_json["labels"] = requests.get(proj_url+"labels/", headers=headers).json()
    print("Found {} label(s)".format(len(gl_json["labels"])))
    gl_json["milestones"] = gitlab_batch(proj_url, headers, "milestone", 20)
    gl_json["issues"] = gitlab_batch(proj_url, headers, "issue", 20)
    return gl_json

def main():
    config = utils.read_file_json("./config.json")
    proj_url = utils.end_with(config["gitlab"]["url"],"/") + config["gitlab"]["projId"] + "/"
    gitlab_json = get_gitlab_json(proj_url, config["gitlab"]["token"])
    save_path = utils.end_with(config["save-path"],"/") + "gitlab-{}.json".format(config["gitlab"]["projId"])
    utils.write_file_json(save_path, gitlab_json)

if __name__ == "__main__":main()