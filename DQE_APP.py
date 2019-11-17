import os
import logging
from Common.parser import FB2Parser
from Common.persister import FBPersister


path_root = 'c:\\input\\'

logging.basicConfig(filename='dqe_test.log', level=logging.DEBUG, format=u'%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')


def search_folder(path):
    p = FBPersister()
    logging.info("Checking out a root folder: "+ path)
    for entry in os.listdir(path):
        path_file = path + entry.title()
        file_name = entry.title()
        if entry.lower().endswith('.fb2'):
#            print(file_name)
            logging.info("A FB2 file was found: "+file_name)
            parser = FB2Parser(path_file)
            book = parser.parse()
            p.insert(book)
#        else:
#            print(file_name)
    logging.info("The destination folder scanning was finished")


search_folder(path_root)
