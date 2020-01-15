class Issue:

    identifier = ''
    is_open = True
    description = ''
    list_id = ''
    board_id = ''
    milestone_id = ''
    labels = []
    name = ''
    position = 0
    completed_date = ''
    creation_data = ''

    def __init__(self, data, src_type):
        if src_type.lower() == 'trello':
            self.init_trello(data)
        # TODO: GitLab
        # TODO: Glo
        else:
            raise Exception('Unknown source type {}'.format(src_type))

    def init_trello(self, data):
        self.identifier = data['id']
        self.is_open = not data['closed']
        self.description = data['desc']
        self.list_id = data['idList']
        self.board_id = data['idBoard']
        self.milestone_id = None
        self.name = data['name']
        self.position = data['pos'] if self.is_open else None
        self.completed_date = data['due']  # 2019-03-10T22:08:33.908Z
        self.creation_date = None          # checks lastActivity, but no creation

    def init_gitlab(self, data):
        pass

    def init_glo(self, data):
        pass
