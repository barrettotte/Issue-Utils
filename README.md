# Issue-Utils

Utilities for various issue tracking services including Trello, GitLab, and GitKraken Glo.


## My Issue Tracking
I'm a lone developer so I cram everything I do into two boards.
One is a main board and the other is a giant backlog with too many items in it.

| Service | Time      | Milestones | First Milestone                  | Last Milestone                   | Cards |
| ------- | --------- | ---------- | -------------------------------- | -------------------------------- | ----- |
| GitLab  | 2018-2019 | 37 Weeks   | Week 01: 10/01/2018 - 10/08/2018 | Week 37: 06/09/2019 - 06/16/2019 |  659  |
| Trello  | 2019-2020 | 41 Weeks   | Week 38: 06/16/2019 - 06/23/2019 | Week 79: 06/14/2020 - 06/21/2020 | 1776  |
| Glo     | 2020-?    | ?          | ?                                | ?                                | ?     |

I'm still unsure if I want to make the switch over to Glo...but I have a migration strategy for when I'm ready.


## Trello to Glo
Unfortunately, Trello does not seem to track milestones or issue creation date... 

I made a one-off script (**misc/approx_milestones.py**) to attempt approximating the milestone an issue would have landed in
based on the completion date and some old data I found in my GitLab board. 
Luckily I was completely consistent with my week long milestones so everything seems to line up correctly after executing.

```exporter.py``` -> ```misc/approx_milestones.py``` -> ```importer.py```

This sets up each Glo board 95% of the way there. 
* Closed issues must be archived with the site's UI even though 'archive_date' is populated on each issue.
* Past milestones must be closed. Annoying, but whatever.
* 


## Archive - GitLab to Trello
For my first issue migration, I wrote a set of subpar Python scripts.
I only made a set of scripts for migrating from GitLab to Trello.

```gitlab-export.py``` -> ```trello-gitlab-import.py```

I figured I'd include this for sake of completion.
But, I will be rewriting it at some point to match my current import/export pattern.


## To Do
* Add CLI to Exporter/Importer
* Export from GitKraken Glo
* Import exported issues to MSSQL table
* Rewrite GitLab exporter
* Basic report of all of my milestones


## References
* Trello API reference - https://developers.trello.com/reference/
* GitKraken Glo API references
  * 10 requests/s, 2500 requests/h
  * https://support.gitkraken.com/developers/api/
  * https://gloapi.gitkraken.com/v1/docs/
