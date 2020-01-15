# Issue-Utils

Utilities for various issue tracking services including Trello, GitLab, and GitKraken Glo.

I am addicted to making to do list items.


## My Issue Tracking
Unfortunately, Trello does not track milestones. 
So, after my GitLab migration and my weeks in Trello I did not have milestone data anymore.

I made a one-off script (**misc/approx_milestones.py**) to attempt approximating the milestone an issue would have landed in
based on the completion date and some leftover data I found in my GitLab boards.
Its not perfect, but its better than nothing.


| Service | Time      | Milestones | First Milestone                  | Last Milestone                   |
| ------- | --------- | ---------- | -------------------------------- | -------------------------------- |
| GitLab  | 2018-2019 | 37 Weeks   | Week 01: 10/01/2018 - 10/08/2018 | Week 37: 06/09/2019 - 06/16/2019 |
| Trello  | 2019-2020 | 30 Weeks   | Week 38: 06/16/2019 - 06/23/2019 | Week 68: 01/12/2020 - 01/19/2020 |
| Glo     | 2020-?    | ?          | Week 69: 01/19/2020 - 01/26/2020 | ?                                |


I'm a lone developer so I cram everything into two boards.
One is a main board and the other is a giant backlog.


## Archive - GitLab-Trello
For my first issue migration, I wrote a set of subpar Python scripts.
I only made a set of scripts for migrating from GitLab to Trello.

```python3 gitlab-export.py ; python3 trello-gitlab-import.py```

I figured I'd include this for sake of completion.


## To Do
* Export from GitLab again
* Import to GitKraken Glo
* Export from GitKraken Glo
* Import issues to MSSQL table


## References
* Trello API reference - https://developers.trello.com/reference/
* GitKraken Glo API reference - https://gloapi.gitkraken.com/v1/docs/

