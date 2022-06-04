from sqlalchemy import func
from .base import Base, engine, Users, model_decorator


def initialize_db():
    Base.metadata.create_all(engine)


@model_decorator
def new_user(id: int, name: str, is_admin: bool = False, language: str = 'en', session=None):

    user = Users(id=id, name=name, is_admin=is_admin, language=language)

    session.add(user)
    session.commit()

    return {'ok': True}


@model_decorator
def update_user(id: int, name: str = None, is_admin: bool = None, is_active: bool = None, language: str = None, session=None):

    update = dict()
    if is_admin != None:
        update[Users.is_admin] = is_admin

    if is_active != None:
        update[Users.is_active] = is_active

    if language != None:
        update[Users.language] = language

    if name != None:
        update[Users.name] = name

    session.query(Users).filter(
        Users.id == id).update(update)
    session.commit()

    return {'ok': True}


@model_decorator
def delete_user(id: int, session=None):

    session.query(Users).filter(Users.id == id).delete()
    session.commit()

    return {'ok': True}


@model_decorator
def get_admins(session=None):

    admins_list = session.query(Users).filter(Users.is_admin == True).all()

    return admins_list


@model_decorator
def get_users_list(offset=0, limit=8, session=None):

    users_list = session.query(Users).offset(offset * limit).limit(limit).all()

    total = session.query(func.count(Users.id)).scalar()

    return {
        'paginate': {
            'total': total,
            'limit': limit,
            'offset': offset,
        },
        'list': users_list
    }


@model_decorator
def get_user_info(id, session=None):

    result = session.query(Users).filter(Users.id == id).all()

    if len(result) == 0:
        user_info = 'NOAUTH'
    else:
        user_info = result[0]

    return user_info


@model_decorator
def get_active_users_info(session=None):

    result = session.query(Users).filter(Users.is_active == True).all()

    return result
