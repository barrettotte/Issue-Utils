import os, sys
import utils as utils
from models.issue import Issue
from importers.glo_importer import Glo_Importer

def main():
    config = utils.read_file_json('./config.json')
    export_data = utils.read_file_json(config['export'] + os.sep + 'export.json')
    target = 'glo'   # TODO: Make CLI

    if target == 'glo':
        Glo_Importer(config['glo']).import_boards(export_data)
    else:
        raise Exception("Unsupported target '{}'".format(target))

if __name__ == "__main__":main()