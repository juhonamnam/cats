from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from env import sql_url
import logging

engine = create_engine(sql_url)
logger = logging.getLogger('model')


class SQLConnection:
    def __init__(self):
        self.engine = None
        self.Session = None
        self.logger = logging.getLogger('model')

    def open(self, sql_url):
        self.engine = create_engine(sql_url)
        self.Session = sessionmaker(autocommit=False, bind=self.engine)
        self.engine.connect()
        self.logger.info('SQL Connected')

    def close(self):
        self.Session.close_all()
        self.engine.dispose()
        self.logger.info("SQL Disconnected")


db = SQLConnection()
