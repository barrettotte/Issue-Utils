import os, sys
import utils as utils
from models.issue import Issue
from glo_importer import Glo_Importer

def main():
    config = utils.read_file_json('./config.json')
    out_path = config['export']

    target = 'glo'   # TODO: Make CLI
    importer = None

    if target == 'glo':
        importer = Glo_Importer(config['glo'])
    else:
        raise Exception("Unsupported target '{}'".format(target))
    
    importer.import_boards(utils.read_file_json(out_path + os.sep + 'export.json'))

if __name__ == "__main__":main()