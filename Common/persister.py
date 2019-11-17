import sqlite3
import itertools
import logging


logging.basicConfig(filename='dqe_test.log', level=logging.DEBUG, format=u'%(asctime)s - [%(name)s] - %(levelname)s - %(message)s')


class FBPersister:
    def __init__(self):
        #self._name = ':memory:'
        self._name = 'dqe_test.db'
        self.connection = sqlite3.connect(self._name)
        self.build_books_table()
        self.__hasupper = lambda word: any(char.isupper() for char in word)
        self.__alllower  = lambda word: all(char.islower() for char in word)

    def __commit(self):
        self.connection.commit()

    def get_cursor(self):
        return self.connection.cursor()

    def check_if_exists(self, tablename):
        c = self.get_cursor()
        c.execute("SELECT count(1) FROM sqlite_master WHERE type='table' AND name=:name;", {"name": tablename })
        return c.fetchone()[0] > 0

    def build_books_table(self):
        if not self.check_if_exists('books'):
            logging.info('Creating books table')
            c = self.get_cursor()
            c.execute('''CREATE TABLE books (
                            id INTEGER PRIMARY KEY AUTOINCREMENT, 
                            book_name TEXT NOT NULL, 
                            number_of_paragraph BIGINT, 
                            number_of_words BIGINT, 
                            number_of_letters BIGINT, 
                            words_with_capital_letters BIGINT, 
                            words_in_lowercase BIGINT)''')


    def build_stats_table(self, book, book_id):
        tablename = 'stats_' + str(book_id)
        c = self.get_cursor()
        logging.info('Creating stats table: '+tablename )

        if not self.check_if_exists(tablename):
            c.execute('''CREATE TABLE ''' + tablename + ''' (word TEXT, [count] BIGINT, [uppercase] BIGINT)''')

        logging.info('Inserting values into stats table: '+tablename)
        for k, g in itertools.groupby(book.words, key=lambda word: word.lower()):
            l = list(g)
            length = len(l)
            upper = sum(1 for word in l if self.__hasupper(word))

            #print((k, length, upper))
            c.execute("INSERT INTO " + tablename + " (word, [count], [uppercase]) "
                      "VALUES(:word,:count,:uppercase)",
                      {"word": k, "count": length, "uppercase": upper})

    def insert(self, book):
        c = self.get_cursor()
        logging.info('Inserting values into books table: ' + book.title)
        c.execute("INSERT INTO books(book_name, number_of_paragraph, number_of_words, "
                  "number_of_letters, words_with_capital_letters, words_in_lowercase) "
                  "VALUES (:title, :nofp, :nofw, :nofl, :wwcl, :winl)",
                  {
                      "title" : book.title,
                      "nofp": len(book.texts),
                      "nofw": len(book.words),
                      "nofl": sum(len(word) for word in book.words),
                      "wwcl": sum(1 for word in book.words if self.__hasupper(word)),
                      "winl": sum(1 for word in book.words if self.__alllower(word))
                  })

        lastrowid = c.lastrowid
        self.build_stats_table(book, lastrowid)
        self.__commit()
