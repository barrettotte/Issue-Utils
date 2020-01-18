# Used for exporting to a central model to work from

class Issue():

    def __init__(self, data=None, src_type='*'):
        self.identifier = ''
        self.is_open = True
        self.description = ''
        self.column_id = ''
        self.board_id = ''
        self.milestone_id = ''
        self.labels = []
        self.name = ''
        self.position = 0
        self.completed_date = ''
        self.creation_date = ''

        if src_type == '*':
            self.init_generic(data)
        elif src_type == 'trello':
            self.init_trello(data)
        elif src_type == 'glo':
            self.init_glo(data)
        elif src_type == 'gitlab':
            self.init_gitlab(data)
        else:
            raise Exception('Unknown source type {}'.format(src_type))


    def __dir__(self):
        return ['identifier', 'is_open', 'description', 'column_id', 'board_id',
          'milestone_id', 'labels', 'name', 'position', 'completed_date', 'creation_date']


    def init_generic(self, data):
        for attr in self.__dir__():
            if attr in data:
                self.__dict__[attr] = data[attr]


    def init_trello(self, data):
        self.identifier = data['id']
        self.is_open = not data['closed']
        self.description = data['desc']
        self.column_id = data['idList']
        self.board_id = data['idBoard']
        self.milestone_id = -1
        self.name = data['name']
        self.labels = data['idLabels']
        self.position = data['pos'] if self.is_open else None
        self.completed_date = data['due']  # 2019-03-10T22:08:33.908Z
        self.creation_date = None          # checks lastActivity, but no creation


    def init_gitlab(self, data):
        pass


    def init_glo(self, data):
        pass
