from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from env import sql_url
import logging

Base = declarative_base()
engine = create_engine(sql_url)
logger = logging.getLogger('model')


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    language = Column(String(3))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def model_decorator(model_function):
    def wrapper_function(*args, **kwargs):
        Session = sessionmaker(bind=engine)
        session = Session()

        try:
            result = model_function(*args, **kwargs, session=session)
        except Exception as e:
            logger.error(str(e))
            result = {'ok': False, 'description': e.__str__()}

        session.close()

        return result

    return wrapper_function
