import xml.etree.ElementTree as ET
from Common.book import FBBook
import logging


logging.basicConfig(filename='dqe_test.log', level=logging.DEBUG, format=u'%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')


class FB2Parser:
    def __init__(self, filename):
        self.root = ET.parse(filename).getroot()
        self.cleanup()

    def cleanup(self):
        for element in self.root.iter():
            element.tag = element.tag.partition('}')[-1]

    def parse(self):
        texts = []
        title = self.root.find('./description/title-info/book-title').text
        logging.info('Parsing a book: '+title)
        for p in self.root.findall('./body//p'):
            text = p.text
            if text is not None:
                texts.append(text)
        logging.info('The book was parsed: ' + title)
        return FBBook(title, texts)
