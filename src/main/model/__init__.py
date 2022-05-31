from sqlalchemy import create_engine, Column, Integer, String, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from env import sql_url

Base = declarative_base()
engine = create_engine(sql_url)


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    language = Column(String)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


def initialize_db():
    Base.metadata.create_all(engine)


def new_user(id: int, name: str, is_admin: bool = False, language: str = 'en'):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        user = Users(id=id, name=name, is_admin=is_admin, language=language)

        session.add(user)
        session.commit()

        return '0000'

    except Exception as e:
        print(e)
        session.rollback()

        return '5000'


def update_user(id: int, name: str = None, is_admin: bool = None, is_active: bool = None, language: str = None):
    Session = sessionmaker(bind=engine)
    session = Session()

    update = dict()
    if is_admin != None:
        update[Users.is_admin] = is_admin

    if is_active != None:
        update[Users.is_active] = is_active

    if language != None:
        update[Users.language] = language

    if name != None:
        update[Users.name] = name

    try:
        session.query(Users).filter(
            Users.id == id).update(update)
        session.commit()

        return '0000'

    except Exception as e:
        print(e)
        session.rollback()

        return '5000'


def delete_user(id: int):
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        session.query(Users).filter(Users.id == id).delete()
        session.commit()

        return '0000'

    except Exception as e:
        print(e)
        session.rollback()

        return '5000'


def get_admins():
    Session = sessionmaker(bind=engine)
    session = Session()

    admins_list = session.query(Users).filter(Users.is_admin == True).all()

    session.close()

    return admins_list


def get_users_list(offset=0, limit=8):
    Session = sessionmaker(bind=engine)
    session = Session()

    users_list = session.query(Users).offset(offset * limit).limit(limit).all()

    total = session.query(func.count(Users.id)).scalar()

    session.close()

    return {
        'paginate': {
            'total': total,
            'limit': limit,
            'offset': offset,
        },
        'list': users_list
    }


def get_user_info(id):
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(Users).filter(Users.id == id).all()

    if len(result) == 0:
        user_info = 'NOAUTH'
    else:
        user_info = result[0]

    session.close()

    return user_info


def get_active_users_info():
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(Users).filter(Users.is_active == True).all()

    session.close()

    return result
