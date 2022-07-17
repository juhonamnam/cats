from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    language = Column(String(3))
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
